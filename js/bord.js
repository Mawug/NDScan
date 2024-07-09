document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu li');
    const sections = document.querySelectorAll('.content-section');

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all sections
            sections.forEach(section => section.classList.remove('active'));

            // Get the section ID from the data attribute
            const sectionID = item.getAttribute('data-section');

            // Add active class to the selected section
            document.getElementById(sectionID).classList.add('active');
        });
    });

    document.getElementById('logout').addEventListener('click', function() {
        alert('Vous allez être déconnecté.');
    });

    document.getElementById('download-report').addEventListener('click', function() {
        // Simulate report download
        const link = document.createElement('a');
        link.href = 'rapport.pdf'; // Remplacez par le chemin de votre rapport
        link.download = 'rapport.pdf';
        link.click();
    });
});
