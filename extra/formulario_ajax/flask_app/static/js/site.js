
function verUsuarios(){
    fetch('http://127.0.0.1:5000/usuarios')
        .then(res =>  res.json())
        .then(data => {
            var usuarios = document.getElementById('usuarios');
            for( let i = 0; i < data.length; i++){
                let fila = document.createElement('tr');

                let nombre = document.createElement('td');
                nombre.innerHTML = data[i].nombre;
                fila.appendChild(nombre);
                
                let email = document.createElement('td');
                email.innerHTML = data[i].email;
                fila.appendChild(email);
                usuarios.appendChild(fila);
            }
        })

}
verUsuarios();

