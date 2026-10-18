// Rich-text editor for posts (TipTap, same family as Super Notes).
// Progressive: without JS the plain <textarea> still works and the server
// turns its text into paragraphs. With JS the textarea is hidden and kept in
// sync with the editor's HTML; the server cleans that HTML on save.

import { Editor } from 'https://esm.sh/@tiptap/core@3.31.4';
import StarterKit from 'https://esm.sh/@tiptap/starter-kit@3.31.4';
import { Placeholder } from 'https://esm.sh/@tiptap/extensions@3.31.4';
import Image from 'https://esm.sh/@tiptap/extension-image@3.31.4';

const root = document.querySelector('[data-editor]');
const textarea = root.querySelector('textarea');
const mount = root.querySelector('.editor-mount');
const toolbar = root.querySelector('.editor-toolbar');
const status = document.querySelector('.editor-status');
const fileInput = root.querySelector('[data-image-input]');
const csrf = root.closest('form').querySelector('[name=csrfmiddlewaretoken]').value;

const looksLikeHtml = /^\s*<(p|h2|h3|ul|ol|pre|blockquote|hr|img)\b/i;
const escape = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const initial = looksLikeHtml.test(textarea.value)
  ? textarea.value
  : textarea.value.split(/\n\s*\n/).filter((b) => b.trim()).map((b) => `<p>${escape(b).replace(/\n/g, '<br>')}</p>`).join('');

const editor = new Editor({
  element: mount,
  content: initial,
  extensions: [
    StarterKit.configure({
      heading: { levels: [2, 3] },
      link: { openOnClick: false, autolink: true, protocols: ['mailto'] },
    }),
    Placeholder.configure({ placeholder: 'Start your blog…' }),
    Image,
  ],
  editorProps: {
    // Pasted or dropped image files are uploaded instead of embedded
    handlePaste: (view, event) => uploadFiles(event.clipboardData?.files),
    handleDrop: (view, event) => {
      const at = view.posAtCoords({ left: event.clientX, top: event.clientY });
      return uploadFiles(event.dataTransfer?.files, at?.pos);
    },
  },
  onUpdate: sync,
  onSelectionUpdate: refresh,
});

let notice = '';

function sync() {
  textarea.value = editor.isEmpty ? '' : editor.getHTML();
  const chars = editor.getText().length;
  status.textContent = notice || `${chars} characters${chars < 3000 ? ` · ${3000 - chars} more to publish` : ''}`;
  refresh();
}

// Toolbar: each button names a command; active state follows the cursor
const commands = {
  bold: (c) => c.toggleBold(),
  italic: (c) => c.toggleItalic(),
  underline: (c) => c.toggleUnderline(),
  strike: (c) => c.toggleStrike(),
  h2: (c) => c.toggleHeading({ level: 2 }),
  h3: (c) => c.toggleHeading({ level: 3 }),
  bulletList: (c) => c.toggleBulletList(),
  orderedList: (c) => c.toggleOrderedList(),
  blockquote: (c) => c.toggleBlockquote(),
  code: (c) => c.toggleCode(),
  codeBlock: (c) => c.toggleCodeBlock({ language: language.value }),
  hr: (c) => c.setHorizontalRule(),
  undo: (c) => c.undo(),
  redo: (c) => c.redo(),
};
const isActive = {
  bold: () => editor.isActive('bold'),
  italic: () => editor.isActive('italic'),
  underline: () => editor.isActive('underline'),
  strike: () => editor.isActive('strike'),
  h2: () => editor.isActive('heading', { level: 2 }),
  h3: () => editor.isActive('heading', { level: 3 }),
  bulletList: () => editor.isActive('bulletList'),
  orderedList: () => editor.isActive('orderedList'),
  blockquote: () => editor.isActive('blockquote'),
  code: () => editor.isActive('code'),
  codeBlock: () => editor.isActive('codeBlock'),
  link: () => editor.isActive('link'),
};
const language = toolbar.querySelector('[data-language]');

toolbar.addEventListener('click', (e) => {
  const button = e.target.closest('button[data-cmd]');
  if (!button) return;
  e.preventDefault();
  const cmd = button.dataset.cmd;
  if (cmd === 'link') return setLink();
  if (cmd === 'image') return fileInput.click();
  commands[cmd](editor.chain().focus()).run();
});

// Changing the language re-labels the code block the cursor is in
language.addEventListener('change', () => {
  if (editor.isActive('codeBlock')) {
    editor.chain().focus().updateAttributes('codeBlock', { language: language.value }).run();
  }
});

function setLink() {
  const previous = editor.getAttributes('link').href || 'https://';
  const href = window.prompt('Link address (leave empty to remove)', previous);
  if (href === null) return;
  const chain = editor.chain().focus().extendMarkRange('link');
  (href.trim() ? chain.setLink({ href: href.trim() }) : chain.unsetLink()).run();
}

fileInput.addEventListener('change', () => {
  uploadFiles(fileInput.files);
  fileInput.value = '';
});

function uploadFiles(files, pos) {
  const images = [...(files || [])].filter((f) => f.type.startsWith('image/'));
  if (!images.length) return false;
  images.forEach((file) => upload(file, pos));
  return true;
}

async function upload(file, pos) {
  setNotice(`Uploading ${file.name}…`);
  const body = new FormData();
  body.append('image', file);
  try {
    const res = await fetch(root.dataset.uploadUrl, {
      method: 'POST',
      body,
      headers: { 'X-CSRFToken': csrf },
      credentials: 'same-origin',
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || 'Upload failed.');
    const alt = (window.prompt('Describe the image for readers who can’t see it (optional)', '') || '').trim();
    const chain = editor.chain().focus();
    (pos == null ? chain : chain.setTextSelection(pos)).setImage({ src: data.url, alt }).run();
    // The new image is left selected, so typing would replace it: continue on a line below
    if (editor.state.selection.node?.type.name === 'image') editor.chain().createParagraphNear().focus().run();
    setNotice('');
  } catch (err) {
    setNotice(err.message);
    setTimeout(() => setNotice(''), 6000);
  }
}

function setNotice(text) {
  notice = text;
  sync();
}

function refresh() {
  toolbar.querySelectorAll('button[data-cmd]').forEach((b) => {
    const active = isActive[b.dataset.cmd]?.() ?? false;
    b.classList.toggle('is-active', active);
    b.setAttribute('aria-pressed', String(active));
  });
  if (editor.isActive('codeBlock')) {
    language.value = editor.getAttributes('codeBlock').language || 'text';
  }
}

textarea.hidden = true;
textarea.required = false; // a hidden required field would block submit; the server checks length
toolbar.hidden = false;
root.classList.add('editor');
sync();
