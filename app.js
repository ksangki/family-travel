const menu = document.querySelector('#menu');
const nav = document.querySelector('#nav');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? '메뉴 닫기' : '메뉴 열기';
  nav?.classList.toggle('open', open);
});
nav?.addEventListener('click', event => {
  if (event.target.closest('a')) {
    nav.classList.remove('open');
    menu?.setAttribute('aria-expanded', 'false');
    if (menu) menu.textContent = '메뉴 열기';
  }
});
const viewer = document.querySelector('#viewer');
document.addEventListener('click', event => {
  const button = event.target.closest('.gallery-photo, #open-photo');
  if (!button || !viewer) return;
  const img = viewer.querySelector('img');
  const caption = button.dataset.caption || '시드니 항구 · 공개 대표 풍경 사진';
  img.src = button.dataset.src || 'assets/sydney-harbour.jpg';
  img.alt = caption;
  viewer.querySelector('#caption').textContent = caption;
  viewer.showModal();
});
document.querySelector('#close-photo')?.addEventListener('click', () => viewer?.close());
viewer?.addEventListener('click', event => {
  if (event.target !== viewer) return;
  const rect = viewer.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();
});
