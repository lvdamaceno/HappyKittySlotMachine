document.addEventListener('DOMContentLoaded', () => {
  const columns = [
    document.getElementById('column1'),
    document.getElementById('column2'),
    document.getElementById('column3')
  ];
  const lever = document.getElementById('lever');
  const messageEl = document.getElementById('message');
  const attemptsCountEl = document.getElementById('attempts-count');
  const coinCountEl = document.getElementById('coin-count');

  let attempts = parseInt(attemptsCountEl.textContent, 10) || 10;
  let coins = parseInt(coinCountEl.textContent, 10) || 0;
  const figures = ['1','2','3','4','5','6','7'];

  function spin() {
    if (attempts <= 0) {
      messageEl.textContent = 'Sem tentativas restantes!';
      return;
    }
    if (coins < 100) {
      messageEl.textContent = 'Moedas insuficientes para jogar!';
      return;
    }
    // Custo de 100 moedas por jogada
    attempts--;
    coins -= 100;
    attemptsCountEl.textContent = attempts;
    coinCountEl.textContent = coins;
    messageEl.textContent = '';

    // Sorteia índices finais
    const results = columns.map(() => Math.floor(Math.random() * figures.length));
    const baseDuration = 2000;

    columns.forEach((col, i) => {
      const duration = baseDuration + i * 500;
      animateColumnSequential(col, results[i], duration);
    });

    // Pós-animation
    setTimeout(() => {
      // Conta aparições do número '3'
      const threeCount = results.filter(i => figures[i] === '3').length;
      let reward = 0;
      if (threeCount === 1) reward = 50;
      if (threeCount === 2) reward = 100;
      if (threeCount === 3) reward = 150;
      coins += reward;
      coinCountEl.textContent = coins;

      if (reward > 0) {
        messageEl.textContent = `Você acertou ${threeCount}x '3' e ganhou ${reward} moedas!`;
      } else if (results.every(r => r === results[0])) {
        messageEl.textContent = 'Parabéns! Você ganhou o jackpot!';
      } else {
        messageEl.textContent = 'Tente novamente.';
      }
    }, baseDuration + 1000);
  }

  /**
   * Anima a coluna sequencialmente, passando por cada figura em ordem, desacelerando até o finalIndex.
   * @param {HTMLElement} column
   * @param {number} finalIndex
   * @param {number} duration Tempo total da animação em ms
   */
  function animateColumnSequential(column, finalIndex, duration) {
    const startTime = performance.now();
    const endTime = startTime + duration;
    const totalFigures = figures.length;
    let position = 0;
    /**
     * Intervalo mínimo e máximo (ms) para controle de velocidade
     */
    const minInterval = 50;    // mais rápido
    const maxInterval = 300;   // mais lento

    function update(now) {
      // Calcula t de 0 a 1
      const t = Math.min((now - startTime) / duration, 1);
      // Intervalo linearmente entre min e max
      const interval = minInterval + (maxInterval - minInterval) * t;

      // Armazena última vez que atualizou em propriedade privada
      if (!column._lastUpdate) column._lastUpdate = now;
      if (now - column._lastUpdate >= interval) {
        position = (position + 1) % totalFigures;
        column.textContent = figures[position];
        column._lastUpdate = now;
      }

      if (now < endTime) {
        requestAnimationFrame(update);
      } else {
        // Garante parada suave no finalIndex
        column.textContent = figures[finalIndex];
        delete column._lastUpdate;
      }
    }

    requestAnimationFrame(update);
  }

  lever.addEventListener('click', spin);
});