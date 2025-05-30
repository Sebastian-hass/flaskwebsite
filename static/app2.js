document.addEventListener('DOMContentLoaded', function() {
    // Menú de navegación
    const menuButton = document.getElementById('menuButton');
    const navMenu = document.getElementById('navMenu');

    menuButton.addEventListener('click', function(event) {
        event.stopPropagation();
        navMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', function(event) {
        if (!navMenu.contains(event.target) && event.target !== menuButton) {
            navMenu.classList.add('hidden');
        }
    });

    // Slider
    const slider = document.querySelector('.slider');
    const items = slider.querySelectorAll('.item');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    let currentIndex = 0;

    function showItem(index) {
        items.forEach((item, i) => {
            item.classList.remove('active');
            if (i === index) {
                item.classList.add('active');
            }
        });
    }

    function nextItem() {
        currentIndex = (currentIndex + 1) % items.length;
        showItem(currentIndex);
    }

    function prevItem() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showItem(currentIndex);
    }

    prevButton.addEventListener('click', prevItem);
    nextButton.addEventListener('click', nextItem);

    // Ajuste del diámetro
    const setDiameter = () => {
        let widthSlider = slider.offsetWidth;
        let heightSlider = slider.offsetHeight;
        let diameter = Math.sqrt(Math.pow(widthSlider, 2) + Math.pow(heightSlider, 2));
        document.documentElement.style.setProperty('--diameter', diameter + 'px');
    }

    setDiameter();
    window.addEventListener('resize', setDiameter);

    // Rotación automática (opcional)
    setInterval(nextItem, 5000);
});

let currentIndex = 0;

const carruselContainer = document.querySelector('.carrusel-container');
const images = document.querySelectorAll('.carrusel-container img');
const totalImages = images.length;

function updateCarrusel() {
    carruselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function autoPlay() {
    currentIndex = (currentIndex + 1) % totalImages;
    updateCarrusel();
}

document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.carousel-slide');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(-${index * 100}%)`;
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    setInterval(nextSlide, 5000); // Cambia de imagen cada 5 segundos
});
