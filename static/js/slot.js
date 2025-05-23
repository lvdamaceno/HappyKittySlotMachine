document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('spin-button');
    const slots = document.querySelector('.slots');
    const cells = document.querySelectorAll('.reel');
    const messageEl = document.getElementById('message');

    button.addEventListener('click', async (e) => {
        e.preventDefault();
        messageEl.textContent = '';
        button.disabled = true;
        slots.classList.remove('win');

        const response = await fetch('/spin');
        const { matrix, win } = await response.json();

        let completed = 0;
        const total = cells.length;

        cells.forEach(cell => {
            const row = Number(cell.dataset.row);
            const col = Number(cell.dataset.col);
            const finalValue = matrix[row][col];
            let elapsed = 0;
            const intervalTime = 50;
            const duration = 1000;

            const timer = setInterval(() => {
                cell.textContent = Math.floor(Math.random() * 7) + 1;
                elapsed += intervalTime;
                if (elapsed >= duration) {
                    clearInterval(timer);
                    cell.textContent = finalValue;
                    completed++;
                    if (completed === total) {
                        if (win) slots.classList.add('win');
                        messageEl.textContent = win
                            ? '🎉 JACKPOT! Você acertou 7-7-7!'
                            : 'Tente novamente!';
                        button.disabled = false;
                    }
                }
            }, intervalTime);
        });
    });
});