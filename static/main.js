const btnDelete = document.querySelectorAll('.btn-delete');

if(btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnDelete.forEach((btn) => {
        btn.addEventListener('click', function(e){
            if(!confirm('Are you sure you want to delete it?')){
                e.preventDefault();    
            }
        });
    });

}