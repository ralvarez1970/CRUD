// Selecionar elemento botao

const botao_API = document.querySelector("#botao_API");


// Definicao de evento

botao_API.addEventListener("click", async function (event) {
    event.preventDefault(); // impede o reload da página
    const usuario = document.querySelector("#usuario").value; // captura o valor digitado
    const dados = await dadosDeGithub(usuario); 
    document.getElementById(`texto_traduzido`).textContent = dados.name;
});


// Funcao que recupera dados GitHub

async function dadosDeGithub(usuario) {
    var resposta = await fetch(`https://api.github.com/users/${usuario}`);
    var dados = await resposta.json();
    return dados;
}
