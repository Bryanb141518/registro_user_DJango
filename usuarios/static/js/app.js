document.getElementById("formUsuario").addEventListener("submit", function (e) {
    e.preventDefault()

    const data = {
        nombre: document.getElementById("nombre").value,
        apellido: document.getElementById("apellido").value,
        correo: document.getElementById("correo").value,
        edad: document.getElementById("edad").value,
        password: document.getElementById("password").value
    }

    fetch("http://127.0.0.1:8000/api/usuarios/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => {
        if (res.ok) {
            // ✅ Respuesta exitosa (200-299)
            return res.json().then(result => {
                alert(result.mensaje || "Usuario registrado correctamente")
                document.getElementById("formUsuario").reset() // Limpiar formulario
            })
        } else {
            // ❌ Error de validación (400, 404, etc.)
            return res.json().then(errors => {
                let errorMessage = "Errores de validación:\n"
                
                // Mostrar todos los errores
                for (let field in errors) {
                    if (Array.isArray(errors[field])) {
                        errorMessage += `${field}: ${errors[field].join(', ')}\n`
                    } else {
                        errorMessage += `${field}: ${errors[field]}\n`
                    }
                }
                
                alert(errorMessage)
            })
        }
    })
    .catch(err => {
        console.error(err)
        alert("Error de conexión")
    })
})