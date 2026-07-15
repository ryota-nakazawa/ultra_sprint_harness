const initialPosts = [
  { id: 1, author: '田中 美咲', initial: '田', tone: 'avatar-coral', meta: '営業・東京 · 12分前', body: 'はじめての配属先で少し緊張しています。\n同じエリアの同期のみなさん、今週どこかでランチしませんか？ #同期ランチ', likes: 8, liked: false, replies: [] },
  { id: 2, author: '鈴木 大輝', initial: '鈴', tone: 'avatar-mint', meta: '開発・大阪 · 38分前', body: '今日の研修で聞いた「まずは小さく試す」という言葉が印象に残りました。\nみなさんの学びもぜひ聞かせてください！ #研修の学び', likes: 12, liked: false, replies: [{ author: '山本 健太', body: '私も同じメモを取りました！' }] },
  { id: 3, author: '山本 健太', initial: '山', tone: 'avatar-yellow', meta: '企画・名古屋 · 1時間前', body: '通勤時間に読める、おすすめの本やポッドキャストを募集しています。 #おすすめの本', likes: 5, liked: false, replies: [] }
];

let posts = [...initialPosts];
const feed = document.querySelector('#feed');
const template = document.querySelector('#postTemplate');
const postText = document.querySelector('#postText');
const postButton = document.querySelector('#postButton');
const charCount = document.querySelector('#charCount');
const formMessage = document.querySelector('#formMessage');

function renderPosts() {
  feed.innerHTML = '';
  posts.forEach((post) => {
    const node = template.content.cloneNode(true);
    const article = node.querySelector('.post');
    article.dataset.id = post.id;
    const avatar = node.querySelector('.post-avatar');
    avatar.textContent = post.initial;
    avatar.classList.add(post.tone);
    node.querySelector('.post-author').textContent = post.author;
    node.querySelector('.post-meta').textContent = post.meta;
    node.querySelector('.post-body').textContent = post.body;
    const likeButton = node.querySelector('.like-button');
    likeButton.classList.toggle('liked', post.liked);
    likeButton.querySelector('span').textContent = post.liked ? '♥' : '♡';
    likeButton.querySelector('.like-count').textContent = post.likes;
    node.querySelector('.reply-count').textContent = post.replies.length || '';
    const replies = node.querySelector('.replies');
    post.replies.forEach((reply) => {
      const replyNode = document.createElement('p');
      replyNode.className = 'reply';
      replyNode.innerHTML = `<strong>${escapeHtml(reply.author)}</strong>${escapeHtml(reply.body)}`;
      replies.appendChild(replyNode);
    });
    feed.appendChild(node);
  });
}

function escapeHtml(value) { const div = document.createElement('div'); div.textContent = value; return div.innerHTML; }

function updateComposer() {
  const length = postText.value.length;
  charCount.textContent = `${length} / 280`;
  charCount.style.color = length > 260 ? '#c13c31' : '';
  postButton.disabled = !postText.value.trim() || length > 280;
  formMessage.textContent = '';
}

postText.addEventListener('input', updateComposer);
postButton.addEventListener('click', () => {
  const body = postText.value.trim();
  if (!body || body.length > 280) { formMessage.textContent = '1〜280文字で入力してください。'; return; }
  posts.unshift({ id: Date.now(), author: '佐藤 花子', initial: '佐', tone: 'avatar-blue', meta: 'たった今', body, likes: 0, liked: false, replies: [] });
  postText.value = '';
  updateComposer();
  renderPosts();
});

feed.addEventListener('click', (event) => {
  const article = event.target.closest('.post');
  if (!article) return;
  const post = posts.find((item) => item.id === Number(article.dataset.id));
  if (event.target.closest('.like-button')) { post.liked = !post.liked; post.likes += post.liked ? 1 : -1; renderPosts(); }
  if (event.target.closest('.reply-button')) { const box = article.querySelector('.reply-box'); box.hidden = !box.hidden; if (!box.hidden) box.querySelector('input').focus(); }
  if (event.target.closest('.reply-submit')) {
    const input = article.querySelector('.reply-input'); const body = input.value.trim();
    if (body) { post.replies.push({ author: '佐藤 花子', body }); renderPosts(); }
  }
});

document.querySelector('#quickCompose').addEventListener('click', () => { postText.focus(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
document.querySelectorAll('.follow').forEach((button) => button.addEventListener('click', () => { button.classList.toggle('following'); button.textContent = button.classList.contains('following') ? 'フォロー中' : 'フォロー'; }));
renderPosts();
