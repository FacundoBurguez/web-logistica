// Mensaje de carga
console.log("Sitio logístico cargado");

// Scroll suave para navegación de enlaces internos
document.querySelectorAll('a.nav-link').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Simulación de respuestas del bot demo
function simulateBot() {
  const input = document.getElementById("bot-input");
  const chat = document.getElementById("chat-box");
  const message = input.value.trim().toLowerCase();

  if (message === "") return;

  const userMsg = `<div><strong>👤 Usuario:</strong> ${input.value}</div>`;
  let botResponse = "";

  if (message.includes("servicio") || message.includes("ofrecés") || message.includes("hacés")) {
    botResponse = "Ofrezco consultoría logística, automatización de tareas y desarrollo de herramientas web.";
  } else if (message.includes("automatización") || message.includes("bot")) {
    botResponse = "Puedo crear bots que respondan en WhatsApp, correo o web, según lo que necesites.";
  } else if (message.includes("precio") || message.includes("costo") || message.includes("tarifa")) {
    botResponse = "Cada proyecto tiene un enfoque distinto, pero puedo darte una propuesta clara tras un breve diagnóstico.";
  } else if (message.includes("contacto") || message.includes("whatsapp") || message.includes("email")) {
    botResponse = "Podés escribirme directo por WhatsApp con el botón verde o desde la sección de contacto.";
  } else {
    botResponse = "Gracias por tu consulta. Te puedo ayudar con soluciones logísticas personalizadas 🙂";
  }

  chat.innerHTML += userMsg + `<div><strong>🤖 Bot:</strong> ${botResponse}</div>`;
  chat.scrollTop = chat.scrollHeight;
  input.value = "";
}
