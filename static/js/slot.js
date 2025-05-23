// Slot-machine realista: roldana gira dentro de cada coluna

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('spin-button');
  const slots = document.querySelector('.slots');
  const messageEl = document.getElementById('message');
  const columns = Array.from(document.querySelectorAll('.column'));
  const reelHeight = 80;
  const cycles = 2;         // quantas voltas completas de 1 a 7
  const stepTime = 100;      // ms por número

  button.addEventListener('click', async e => {
    e.preventDefault();
    button.disabled = true;
    messageEl.textContent = '';
    slots.classList.remove('win');

    const response = await fetch('/spin');
    const { matrix, win } = await response.json();
    let finished = 0;

    columns.forEach((colEl, colIndex) => {
      // Cria container interno para reels e insere sequência
      const container = document.createElement('div');
      container.className = 'reel-container';

      // Sequência fixa de 1 a 7, repetida, e valores finais
      const seq = [];
      for (let c = 0; c < cycles; c++) {
        for (let n = 1; n <= 7; n++) seq.push(n);
      }
      // Valores finais: matrix[0][col], matrix[1][col], matrix[2][col]
      seq.push(matrix[0][colIndex], matrix[1][colIndex], matrix[2][colIndex]);

      // Preenche o container
      seq.forEach(num => {
        const reel = document.createElement('div');
        reel.className = 'reel';
        reel.textContent = num;
        container.appendChild(reel);
      });

      // Limpa coluna e adiciona container e highlight
      colEl.innerHTML = '';
      colEl.appendChild(container);
      const highlight = document.createElement('div');
      highlight.className = 'highlight';
      colEl.appendChild(highlight);

      // Calcula translado
      const totalHeight = seq.length * reelHeight;
      container.style.transform = 'translateY(0)';
      // Força reflow para aplicar estilo antes da transição
      container.getBoundingClientRect();
      container.style.transition = `transform ${stepTime * seq.length}ms ease-out`;
      container.style.transform = `translateY(-${totalHeight - reelHeight * 3}px)`;

      // Ao fim da animação
      container.addEventListener('transitionend', () => {
        // Restaura estrutura estática com 3 reels finais
        colEl.innerHTML = '';
        matrix.forEach((rowArr, r) => {
          const node = document.createElement('div');
          node.className = 'reel';
          node.textContent = rowArr[colIndex];
          colEl.appendChild(node);
        });
        // Re-anexa highlight
        const hl = document.createElement('div');
        hl.className = 'highlight';
        colEl.appendChild(hl);

        finished++;
        if (finished === columns.length) {
          if (win) slots.classList.add('win');
          messageEl.textContent = win
            ? '🎉 JACKPOT! Você acertou 7-7-7!'
            : 'Tente novamente!';
          button.disabled = false;
        }
      }, { once: true });
    });
  });
});