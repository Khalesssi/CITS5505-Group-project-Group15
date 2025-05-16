// This is used in the home page
// This is the chatbot script
const chatbotFlow = {
  start: {
    message: [
      "{{name}} Welcome to Best Care! This is the best support platform in Western Australia. Nice to meet you!",
      "{{name}} What can I help you today?",
    ],
    options: [
      { label: "I want to know more about Best Care", next: "know_more" },
      { label: "I want to join Best Care", next: "join" },
      { label: "I'm already a member of Best Care", next: "member" },
    ],
  },
  know_more: {
    message: ["What you want to know about Best Care?"],
    options: [
      { label: "I want to know about your service", next: "know_service" },
      { label: "Just browse this website", action: "close" },
    ],
  },
  know_service: {
    message: [
      "Best Care was established in April 2025. We are the top NDIS provider platform in Western Australia, with a professional team of Support Workers and Therapists.",
      "Our platform requires Support Workers to submit daily client data. The backend automatically visualizes this data to help therapists update support plans in a timely manner and continuously improve client outcomes.",
    ],
    options: [
      {
        label: "I want to learn about the Upload feature",
        action: "redirect",
        url: "/#Upload",
      },
      {
        label: "I want to learn about the Data Visualization feature",
        action: "redirect",
        url: "/#Visualise",
      },
      {
        label: "I want to learn about the Share feature",
        action: "redirect",
        url: "/#Share",
      },
    ],
  },

  join: {
    message: ["Why you want to Join Best Care?"],
    options: [
      {
        label: "I'm a support worker and looking for a new job opportunity",
        next: "join_worker",
      },
      {
        label: "I'm a NDIS therapist and looking for a new job opportunity",
        next: "join_worker",
      },
      {
        label: "I'm a guardian looking for a new NDIS provider.",
        next: "join_guardian",
      },
    ],
  },
  join_worker: {
    message: [
      "{{name}} You can click the Get Started button on the top of the navigation,",
      "or just click on the button below:",
    ],
    button: { text: "Get Started", url: "/register" },
  },
  join_guardian: {
    message: [
      "You can click the Get Started button on the top of the navigation,",
      "or just click on the button below to create a new account.",
      "If you don't know how Best Care works, we can contact you.",
      "Would you like to be contacted by email or SMS?",
    ],
    options: [
      { label: "I want to use email", next: "collect_email" },
      { label: "I want to use SMS", next: "collect_phone" },
    ],
  },
  collect_email: {
    message: ["{{name}} Please enter your email address:"],
    input: { placeholder: "Enter your email", next: "collect_name" },
  },
  collect_phone: {
    message: ["{{name}} Please enter your phone number:"],
    input: { placeholder: "Enter your phone number", next: "collect_name" },
  },
  collect_name: {
    message: [
      "What do you want us to call you? Please leave your name in the texting place.",
    ],
    input: { placeholder: "Enter your name", next: "thanks" },
  },
  thanks: {
    message: [
      "{{name}}, thank you for providing these information. Our staff will contact you soon.",
    ],
  },
};

// Core Chatbot Functions
const bot = {
  state: "start",
  userData: {},
  container: document.getElementById("chatbot-messages"),

  showTyping(callback) {
    const bubble = document.createElement("div");
    bubble.textContent = "...";
    bubble.className = "text-gray-500 animate-pulse mb-1";
    bot.container.appendChild(bubble);
    bot.container.scrollTop = bot.container.scrollHeight;
    setTimeout(() => {
      bubble.remove();
      callback();
    }, 800);
  },

  printMessages(messages, cb) {
    if (!messages || messages.length === 0) return cb();
    const [first, ...rest] = messages;
    bot.showTyping(() => {
      const msg = document.createElement("div");
      msg.className = "text-gray-700 bg-gray-100 p-2 rounded mb-1";
      msg.textContent = first.includes("{{name}}")
        ? first.replace("{{name}}", bot.userData.name || "")
        : first;
      bot.container.appendChild(msg);
      bot.container.scrollTop = bot.container.scrollHeight;
      bot.printMessages(rest, cb);
    });
  },

  printOptions(options) {
    options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className =
        "text-sm bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-3 py-1 m-1 rounded";
      btn.textContent = opt.label;
      btn.onclick = () => {
        if (opt.action !== "redirect") {
          const user = document.createElement("div");
          user.className = "text-right text-blue-700 mb-1";
          user.textContent = opt.label;
          bot.container.appendChild(user);
          bot.container.scrollTop = bot.container.scrollHeight;
        }
        if (opt.next) bot.transition(opt.next);
        if (opt.action === "redirect") window.location.href = opt.url;
        if (opt.action === "close") bot.hide();
      };
      bot.container.appendChild(btn);
    });
  },

  transition(state) {
    bot.state = state;
    const step = chatbotFlow[state];
    bot.printMessages(step.message, () => {
      if (step.options) bot.printOptions(step.options);
      if (step.button) {
        const btn = document.createElement("a");
        btn.href = step.button.url;
        btn.textContent = step.button.text;
        btn.className =
          "inline-block mt-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded";
        bot.container.appendChild(btn);
      }
      if (step.input) {
        const input = document.createElement("input");
        input.placeholder = step.input.placeholder;
        input.className = "w-full border mt-2 rounded px-2 py-0.5 text-sm";
        input.onkeydown = (e) => {
          if (e.key === "Enter" && input.value.trim() !== "") {
            const val = input.value.trim();
            const isEmail = /\S+@\S+\.\S+/.test(val);
            const isPhone = /^04\d{8}$/.test(val);

            // Check phone number and email format
            if (bot.state === "collect_name") {
              bot.userData.name = val;
              appendUser(val);
              bot.transition(step.input.next);
            } else if (
              bot.state === "collect_email" ||
              bot.state === "collect_phone"
            ) {
              const valid =
                (bot.state === "collect_email" && isEmail) ||
                (bot.state === "collect_phone" && isPhone);

              if (!valid) {
                bot.printMessages([
                  "{{name}} Invalid format. Please re-enter.",
                ]);
                return;
              }

              bot.userData.contact = val;
              appendUser(val);
              bot.transition(step.input.next);
            }
          }
        };
        bot.container.appendChild(input);
        input.focus();
      }
    });

    function appendUser(text) {
      const user = document.createElement("div");
      user.className = "text-right text-blue-700 mb-1";
      user.textContent = text;
      bot.container.appendChild(user);
      bot.container.scrollTop = bot.container.scrollHeight;
    }
  },

  show() {
    const popup = document.getElementById("chatbot-popup");
    popup.classList.remove("hidden");
    popup.classList.add("w-96", "h-[500px]");
    bot.container.innerHTML = "";
    bot.transition("start");
  },
  hide() {
    document.getElementById("chatbot-popup").classList.add("hidden");
  },
};

document.getElementById("chatbot-toggle").onclick = bot.show;
document.getElementById("chatbot-close").onclick = bot.hide;
