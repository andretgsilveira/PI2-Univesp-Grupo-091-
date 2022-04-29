function copiarTexto() {
    var textoCopiado = document.getElementById("link");
    textoCopiado.select();
    document.execCommand("Copy");
    alert("Texto Copiado: " + textoCopiado.value);
}