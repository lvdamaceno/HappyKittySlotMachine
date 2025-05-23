document.addEventListener('DOMContentLoaded', () => {
  const columns = [
    document.getElementById('column1'),
    document.getElementById('column2'),
    document.getElementById('column3')
  ];
  const lever = document.getElementById('lever');
  const messageEl = document.getElementById('message');
  const attemptsEl = document.getElementById('attempts-count');
  const coinEl = document.getElementById('coin-count');
  const confettiCanvas = document.getElementById('confetti-canvas');

  let attempts = parseInt(attemptsEl.textContent, 10);
  let coins = parseInt(coinEl.textContent, 10);

  const icons = ['star', 'heart', 'diamond', 'club', 'spade', 'crown', 'bell'];

  function resizeCanvas() {
    confettiCanvas.width = window.innerWidth;
    confettiCanvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // Exibe ícones iniciais ao carregar a página
  function initializeSlots() {
    columns.forEach(col => {
      const idx = Math.floor(Math.random() * icons.length);
      col.innerHTML = `<i class="ph ph-${icons[idx]}"></i>`;
    });
  }
  initializeSlots();

  function spin() {
    if (attempts <= 0) { messageEl.textContent = 'Sem tentativas!'; return; }
    if (coins < 100)   { messageEl.textContent = 'Moedas insuficientes!'; return; }

    // Desativa o botão durante o giro
    lever.disabled = true;
    lever.classList.add('lever-active');
    setTimeout(() => lever.classList.remove('lever-active'), 300);

    attempts--;
    coins -= 100;
    attemptsEl.textContent = attempts;
    coinEl.textContent = coins;
    messageEl.textContent = '';

    const results = columns.map(() => Math.floor(Math.random() * icons.length));
    const baseDuration = 2000;

    columns.forEach(col => col.classList.remove('winner'));

    columns.forEach((col, i) => animateColumn(col, results[i], baseDuration + i * 500));

    setTimeout(() => {
      const hits = results.filter(i => icons[i] === 'diamond').length;
      const reward = {1:50, 2:100, 3:150}[hits] || 0;

      coins += reward;
      coinEl.textContent = coins;

      if (reward > 0) {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      }

      columns.forEach((col, i) => {
        if (icons[results[i]] === 'diamond') {
          col.classList.add('winner');
        }
      });

      if (reward > 0) {
        const gain = document.createElement('span');
        gain.textContent = `+${reward}`;
        gain.className = 'coin-gain';
        document.querySelector('.coins').appendChild(gain);
        setTimeout(() => gain.remove(), 1000);
      }

      if (hits > 0) {
        messageEl.textContent = `Você acertou ${hits}x \"diamond\" e ganhou ${reward} moedas!`;
      } else if (results.every(r => r === results[0])) {
        messageEl.textContent = 'Jackpot! Parabéns!';
      } else {
        messageEl.textContent = 'Tente novamente.';
      }

      // Reativa o botão após o giro
      lever.disabled = false;
    }, baseDuration + 1000);
  }

  function animateColumn(column, finalIndex, duration) {
    const start = performance.now();
    let pos = 0;
    const total = icons.length;

    function update(now) {
      const t = Math.min((now - start) / duration, 1);
      const interval = 50 + (300 - 50) * t;
      if (!column._lastUpdate) column._lastUpdate = now;
      if (now - column._lastUpdate >= interval) {
        pos = (pos + 1) % total;
        column.innerHTML = `<i class="ph ph-${icons[pos]}"></i>`;
        column._lastUpdate = now;
      }
      if (now < start + duration) {
        requestAnimationFrame(update);
      } else {
        column.innerHTML = `<i class="ph ph-${icons[finalIndex]}"></i>`;
        delete column._lastUpdate;
      }
    }

    requestAnimationFrame(update);
  }

  lever.addEventListener('click', spin);
});