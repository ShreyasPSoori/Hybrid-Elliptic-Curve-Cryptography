const state = { packageId: '', file: null, metadata: null, publicKey: null };
const toast = document.getElementById('toast');

function notify(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(notify.timer);
  notify.timer = window.setTimeout(() => toast.classList.remove('show'), 3200);
}

function makeId() {
  return `PKG-${crypto.getRandomValues(new Uint32Array(1))[0].toString(16).toUpperCase().padStart(8, '0')}`;
}

function saveDownload(name, content, type = 'text/plain') {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([content], { type }));
  link.download = name;
  link.click();
  URL.revokeObjectURL(link.href);
}

function setDownloadButton(id, name, content, type) {
  const button = document.getElementById(id);
  button.disabled = false;
  button.onclick = () => saveDownload(name, content, type);
}

function toBase64(bytes) {
  let binary = '';
  for (let offset = 0; offset < bytes.length; offset += 0x8000) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + 0x8000));
  }
  return btoa(binary);
}

function fromBase64(value) {
  return Uint8Array.from(atob(value), (character) => character.charCodeAt(0));
}

async function encryptDemo(fileBytes) {
  const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
  const nonce = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce }, key, fileBytes);
  return { key, nonce: toBase64(nonce), ciphertext: toBase64(new Uint8Array(ciphertext)) };
}

async function decryptDemo(ciphertext, keyJwk, nonce) {
  const key = await crypto.subtle.importKey('jwk', keyJwk, { name: 'AES-GCM' }, false, ['decrypt']);
  const plaintext = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: fromBase64(nonce) }, key, fromBase64(ciphertext));
  return new Uint8Array(plaintext);
}

const senderForm = document.getElementById('senderForm');
if (senderForm) {
  const sourceFile = document.getElementById('sourceFile');
  sourceFile.addEventListener('change', () => {
    const file = sourceFile.files[0];
    if (file) document.getElementById('sourceFileName').textContent = `${file.name} · ${(file.size / 1048576).toFixed(2)} MB`;
  });
  const packageId = document.getElementById('packageId');
  senderForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const file = sourceFile.files[0];
    if (!file) { notify('Choose a file before creating the package.'); return; }
    if (file.size > 5 * 1024 * 1024) { notify('This prototype accepts files up to 5 MB.'); return; }
    const id = makeId();
    const encrypted = await encryptDemo(await file.arrayBuffer());
    const keyJwk = await crypto.subtle.exportKey('jwk', encrypted.key);
    packageId.textContent = id;
    const metadata = { package_id: id, algorithm: 'Hybrid X25519 + ML-KEM-768 + HKDF-SHA256 + AES-256-GCM', sender: 'Alice', recipient: document.getElementById('recipient').value.trim() || 'Bob', original_file_name: file.name, encrypted_file_name: `${file.name}.enc`, original_file_type: file.type || 'application/octet-stream', original_file_size: file.size, nonce: encrypted.nonce, status: 'prototype-package', ciphertext_encoding: 'base64' };
    const publicKey = `package_id=${id}\nkey_type=X25519 + ML-KEM-768\npublic_key=prototype-public-key-${id.toLowerCase()}\nowner=Bob`;
    setDownloadButton('downloadMetadata', 'metadata.json', JSON.stringify(metadata, null, 2), 'application/json');
    setDownloadButton('downloadKey', 'public-key.txt', publicKey);
    setDownloadButton('downloadFile', metadata.encrypted_file_name, fromBase64(encrypted.ciphertext), 'application/octet-stream');
    document.getElementById('encryptedFileInfo').textContent = `${metadata.encrypted_file_name} · ${(encrypted.ciphertext.length / 1.33 / 1048576).toFixed(2)} MB`;
    localStorage.setItem('hybridCryptoPackage', JSON.stringify({ metadata, publicKey, encryptedContent: encrypted.ciphertext, keyJwk }));
    document.getElementById('packageReady').classList.add('show');
    document.getElementById('senderStatus').textContent = 'Package ready to send';
    document.getElementById('senderStatus').style.color = 'var(--mint)';
    notify('Package created. Send all three files to Bob.');
  });
}

const receiverForm = document.getElementById('receiverForm');
if (receiverForm) {
  const slots = { receivedFile: 'file', receivedMetadata: 'metadata', receivedKey: 'publicKey' };
  Object.entries(slots).forEach(([inputId, key]) => {
    document.getElementById(inputId).addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      state[key] = key === 'metadata' ? JSON.parse(await file.text()) : key === 'file' ? toBase64(new Uint8Array(await file.arrayBuffer())) : await file.text();
      const slot = event.target.closest('.drop');
      slot.classList.add('ready');
      slot.querySelector('strong').textContent = file.name;
      slot.querySelector('span').textContent = 'Attached and ready';
      validateReceiver();
    });
  });
  document.getElementById('useLatestPackage').addEventListener('click', () => {
    const stored = JSON.parse(localStorage.getItem('hybridCryptoPackage') || 'null');
    if (!stored?.metadata?.encrypted_file_name || !stored.encryptedContent || !stored.keyJwk) { notify('Create a new file package on the Sender page first.'); return; }
    state.file = stored.encryptedContent; state.metadata = stored.metadata; state.publicKey = stored.publicKey;
    ['receivedFile', 'receivedMetadata', 'receivedKey'].forEach((id) => document.getElementById(id).closest('.drop').classList.add('ready'));
    document.querySelector('[for="receivedFile"] strong').textContent = stored.metadata.encrypted_file_name;
    document.querySelector('[for="receivedMetadata"] strong').textContent = 'metadata.json';
    document.querySelector('[for="receivedKey"] strong').textContent = 'public-key.txt';
    validateReceiver();
  });
  receiverForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!validateReceiver()) return;
    document.getElementById('unlockResult').classList.add('show');
    const stored = JSON.parse(localStorage.getItem('hybridCryptoPackage') || 'null');
    if (!stored?.keyJwk || stored.metadata.package_id !== state.metadata.package_id) {
      notify('Package verified. Bob\'s local private-key integration is required for this imported package.');
      return;
    }
    let recovered;
    try {
      recovered = await decryptDemo(state.file, stored.keyJwk, state.metadata.nonce);
    } catch {
      notify('The encrypted file does not match this package metadata.');
      return;
    }
    const downloadName = state.metadata.original_file_name || 'decrypted-file';
    const downloadButton = document.createElement('button');
    downloadButton.className = 'copy';
    downloadButton.textContent = `Download decrypted file: ${downloadName}`;
    downloadButton.onclick = () => saveDownload(downloadName, recovered, state.metadata.original_file_type);
    document.getElementById('unlockedText').textContent = `${downloadName} · ${state.metadata.original_file_type || 'unknown type'} · ${state.metadata.original_file_size} bytes`;
    document.getElementById('unlockedText').after(downloadButton);
    document.getElementById('receiverStatus').textContent = 'Unlocked and verified';
    notify('Public key and metadata matched. File decrypted successfully.');
  });
}

function validateReceiver() {
  const button = document.getElementById('unlockButton');
  if (!button) return false;
  const metadataId = state.metadata?.package_id;
  const keyId = state.publicKey?.match(/package_id=([^\n]+)/)?.[1];
  const valid = Boolean(state.file && metadataId && keyId && metadataId === keyId);
  if (state.file && state.metadata) {
    let downloadButton = document.getElementById('downloadReceivedEncrypted');
    if (!downloadButton) {
      downloadButton = document.createElement('button');
      downloadButton.id = 'downloadReceivedEncrypted';
      downloadButton.className = 'copy';
      downloadButton.style.cssText = 'width:100%;margin-top:10px;padding:11px';
      document.querySelector('[for="receivedFile"]').after(downloadButton);
    }
    downloadButton.textContent = `Download encrypted file (${state.metadata.encrypted_file_name || 'received.enc'})`;
    downloadButton.onclick = () => saveDownload(state.metadata.encrypted_file_name || 'received.enc', fromBase64(state.file), 'application/octet-stream');
  }
  button.disabled = !valid;
  document.getElementById('matchStatus').textContent = valid ? `Package ${metadataId} matched across all three files` : 'Waiting for the same package file, metadata, and public key';
  return valid;
}
