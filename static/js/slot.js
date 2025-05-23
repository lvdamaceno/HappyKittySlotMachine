let lastValues = [1, 1, 1];

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('spin-button');
  const slotsContainer = document.querySelector('.slots-container');
  const messageEl = document.getElementById('message');
  const coinEl = document.getElementById('coin-counter');
  const columns = Array.from(document.querySelectorAll('.column'));
  const reelHeight = 80;
  const cycles = 2;
  const stepTime = 100;

  button.addEventListener('click', async e => {
    e.preventDefault();
    button.disabled = true;
    messageEl.textContent = '';
    slotsContainer.classList.remove('win');

    const response = await fetch('/spin');
    const data = await response.json();

    if (data.error) {
      messageEl.textContent = data.error;
      coinEl.textContent = `Moedas: ${data.coins}`;
      return;
    }

    const { matrix, win, bonus, coins } = data;
    coinEl.textContent = `Moedas: ${coins}`;

    let finished = 0;

    columns.forEach((colEl, idx) => {
      setTimeout(() => {
        const container = document.createElement('div');
        container.className = 'reel-container';

        const seq = [];
        let start = lastValues[idx];
        for (let c = 0; c < cycles * 7; c++) {
          seq.push(((start + c - 1) % 7) + 1);
        }
        seq.push(matrix[0][idx], matrix[1][idx], matrix[2][idx]);
        lastValues[idx] = matrix[1][idx];

        seq.forEach(val => {
          const div = document.createElement('div');
          div.className = 'reel';
          div.textContent = val;
          container.appendChild(div);
        });

        colEl.innerHTML = '';
        colEl.appendChild(container);

        const totalHeight = seq.length * reelHeight;
        const keyframes = [
          { transform: 'translateY(0)', offset: 0 },
          { transform: `translateY(-${totalHeight * 0.2}px)`, offset: 0.3 },
          { transform: `translateY(-${totalHeight * 0.5}px)`, offset: 0.6 },
          { transform: `translateY(-${totalHeight - reelHeight * 3}px)`, offset: 1 }
        ];

        const animation = container.animate(keyframes, {
          duration: 1200 + idx * 300,
          easing: 'ease-out'
        });

        animation.onfinish = () => {
          colEl.innerHTML = '';
          matrix.forEach(row => {
            const reel = document.createElement('div');
            reel.className = 'reel';
            reel.textContent = row[idx];
            colEl.appendChild(reel);
          });

          finished++;
          if (finished === columns.length) {
            if (win) slotsContainer.classList.add('win');
            let msg = win ? '🎉 JACKPOT! Você acertou 7-7-7!' : 'Tente novamente!';
            if (bonus > 0 && !win) msg += ` + Você ganhou ${bonus} moedas de bônus por aparecer um 3!`;
            messageEl.textContent = msg;
            button.disabled = coins < 100;
          }
        };
      }, idx * 300);
    });
  });
});