document.addEventListener('DOMContentLoaded', () => {
  const columns        = ['column1','column2','column3'].map(id => document.getElementById(id));
  const lever          = document.getElementById('lever');
  const messageEl      = document.getElementById('message');
  const attemptsEl     = document.getElementById('attempts-count');
  const coinEl         = document.getElementById('coin-count');
  const confettiCanvas = document.getElementById('confetti-canvas');

  const icons = ['star','heart','diamond','club','spade','crown','bell'];
  let spinIntervals = [];

  // Inicializa slots aleatoriamente
  function initializeSlots() {
    columns.forEach(col => {
      const idx = Math.floor(Math.random() * icons.length);
      col.innerHTML = `<i class="ph ph-${icons[idx]}"></i>`;
    });
  }

  // Animação inicial ao carregar: spin rápido e parar na posição inicial
  function initialSpin() {
    const initialIcons = columns.map(col => col.querySelector('i').classList[1].split('-')[1]);
    const finalIndices  = initialIcons.map(f => icons.indexOf(f));
    // animação genérica antes de desacelerar
    spinIntervals = columns.map(col =>
      setInterval(() => {
        const rnd = Math.floor(Math.random() * icons.length);
        col.innerHTML = `<i class=\"ph ph-${icons[rnd]}\"></i>`;
      }, 100)
    );
    // depois aplica desaceleração até o ícone inicial
    const baseDuration = 800;
    setTimeout(() => {
      clearSpinIntervals();
      finalIndices.forEach((finalIndex, i) => {
        animateColumn(columns[i], finalIndex, baseDuration + i * 200);
      });
    }, 400);
  }

  initializeSlots();
  initialSpin();

  function shootConfetti() {
    confetti.create(confettiCanvas, { resize: true })({ spread: 60, particleCount: 150 });
  }

  async function spin() {
    lever.disabled = true;
    lever.classList.add('lever-active');
    setTimeout(() => lever.classList.remove('lever-active'), 300);

    messageEl.textContent = 'Girando...';

    // animações genéricas
    spinIntervals = columns.map(col =>
      setInterval(() => {
        const rnd = Math.floor(Math.random() * icons.length);
        col.innerHTML = `<i class=\"ph ph-${icons[rnd]}\"></i>`;
      }, 100)
    );

    try {
      const resp = await fetch('/spin', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'
      });
      if (!resp.ok) {
        const err = await resp.json();
        messageEl.textContent = err.error;
        clearSpinIntervals();
        lever.disabled = false;
        return;
      }

      const { figures, coins, attempts, reward } = await resp.json();
      clearSpinIntervals();

      const finalIndices  = figures.map(f => parseInt(f, 10) - 1);
      const baseDuration2 = 1000;
      columns.forEach(col => col.classList.remove('winner','coin-lose'));

      finalIndices.forEach((finalIndex, i) => {
        animateColumn(columns[i], finalIndex, baseDuration2 + i * 300);
      });

      setTimeout(() => {
        coinEl.textContent     = coins;
        attemptsEl.textContent = attempts;

        if (reward > 0) {
          shootConfetti();
          messageEl.textContent = `Você ganhou ${reward} moedas!`;
          finalIndices.forEach((idx, i) => {
            if (icons[idx] === 'diamond') columns[i].classList.add('winner');
          });
        } else {
          const bellHits = finalIndices.filter(idx => icons[idx] === 'bell').length;
          if (bellHits > 0) {
            const loss = bellHits * 50;
            messageEl.textContent = `Você acertou ${bellHits} sino${bellHits>1?'s':''} e perdeu ${loss} moedas!`;
            finalIndices.forEach((idx,i) => {
              if (icons[idx] === 'bell') columns[i].classList.add('coin-lose');
            });
          } else if (finalIndices.every(idx => icons[idx] === 'crown')) {
            messageEl.textContent = 'Jackpot! Parabéns!';
          } else {
            messageEl.textContent = 'Tente novamente.';
          }
        }
        lever.disabled = false;
      }, baseDuration2 + 400);

    } catch (e) {
      console.error(e);
      messageEl.textContent = 'Erro na comunicação com o servidor.';
      clearSpinIntervals();
      lever.disabled = false;
    }
  }

  function clearSpinIntervals() {
    spinIntervals.forEach(id => clearInterval(id));
    spinIntervals = [];
  }

  function animateColumn(column, finalIndex, duration) {
    const total = icons.length;
    const start = performance.now();
    let pos   = Math.floor(Math.random() * total);

    function update(now) {
      const t = Math.min((now - start) / duration, 1);
      const interval = 50 + (300 - 50) * t;

      if (!column._last) column._last = now;
      if (now - column._last >= interval) {
        pos = (pos + 1) % total;
        column.innerHTML = `<i class=\"ph ph-${icons[pos]}\"></i>`;
        column._last = now;
      }
      if (now < start + duration) {
        requestAnimationFrame(update);
      } else {
        column.innerHTML = `<i class=\"ph ph-${icons[finalIndex]}\"></i>`;
        delete column._last;
      }
    }
    requestAnimationFrame(update);
  }

  lever.addEventListener('click', spin);
});
