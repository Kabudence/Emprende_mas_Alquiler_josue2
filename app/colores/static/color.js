const pickr = Pickr.create({
    el: '.color-picker',
    default: '#FF0000',
    theme: 'classic',
    components: {
        preview: true,
        opacity: true,
        hue: true,
        interaction: {
            input: true,
            save: true
        }
    }
});

pickr.on('save', (color) => {
    const hexColor = color.toHEXA().toString();
    document.getElementById('hexadecimal').value = hexColor;
});

pickr.on('change', (color) => {
    const hexColor = color.toHEXA().toString();
    document.getElementById('hexadecimal').value = hexColor;
});