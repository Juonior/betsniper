const copyButtons = document.querySelectorAll('.copyClipboard');
copyButtons.forEach(button => {
    button.addEventListener('click', () => {
        const matchName = button.getAttribute('data-original-title');
        copyTextToClipboard(matchName);
    });
});

function copyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
}