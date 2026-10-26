const dayFilters = document.querySelectorAll('[data-day-filter]');
const dayCards = document.querySelectorAll('[data-record-day]');
dayFilters.forEach(button => button.addEventListener('click', () => {
  const selected = button.dataset.dayFilter;
  dayFilters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
  let count = 0;
  dayCards.forEach(card => {
    card.hidden = selected !== 'all' && card.dataset.recordDay !== selected;
    if (!card.hidden) count += 1;
  });
  document.querySelector('#day-filter-status').textContent = selected === 'all'
    ? `전체 ${count}개 날짜를 보고 있습니다.` : `${selected} · ${count}개 날짜를 보고 있습니다.`;
}));
const categoryFilter = document.querySelector('#category-filter');
categoryFilter?.addEventListener('change', () => {
  let count = 0;
  document.querySelectorAll('[data-place-category]').forEach(card => {
    card.hidden = categoryFilter.value !== 'all' && card.dataset.placeCategory !== categoryFilter.value;
    if (!card.hidden) count += 1;
  });
  document.querySelector('#place-filter-status').textContent = `${categoryFilter.value === 'all' ? '전체' : categoryFilter.value} ${count}곳`;
});
const mapButtons = document.querySelectorAll('[data-map-point]');
mapButtons.forEach(button => button.addEventListener('click', () => {
  mapButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelectorAll('[data-map-node]').forEach(node => {
    node.classList.toggle('active', node.dataset.mapNode === button.dataset.mapPoint);
  });
  const googleMap = document.querySelector('#google-route-map');
  if (googleMap && button.dataset.mapSrc) googleMap.src = button.dataset.mapSrc;
  document.querySelector('#map-selection').textContent = `${button.textContent} · ${document.querySelector('#google-route-map') ? 'Google 지도' : '기록에서 선택한 장면'}`;
}));
// Reveal all dates before the browser follows an overview link to a daily record.
document.querySelectorAll('[data-overview-day]').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('[data-day-filter="all"]')?.click();
  });
});
