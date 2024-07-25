  
  document.addEventListener("DOMContentLoaded", function() {
      const likeButtons = document.querySelectorAll(".like-btn");

      likeButtons.forEach(button => {
          button.addEventListener("click", function() {
              const postId = this.getAttribute("data-post-id");
              
              fetch(`/like/${postId}`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': '{{ csrf_token() }}'  // Assuming you use CSRF protection
                  },
                  credentials: 'same-origin' // Include cookies in the request
              }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        toggleLikeButton(this);
                        showSmileys();
                    }
                });
          });
      });
  });

  function toggleLikeButton(button) {
      if (button.classList.contains("btn-secondary")) {
          button.classList.remove("btn-secondary");
          button.classList.add("btn-primary");
      } else {
          button.classList.remove("btn-primary");
          button.classList.add("btn-secondary");
      }
  }

  function showSmileys() {
      const smileyContainer = document.getElementById("smiley-container");
      for (let i = 0; i < 10; i++) {
          const smiley = document.createElement("div");
          smiley.classList.add("smiley");
          smiley.innerHTML = "😊";

          // Random position within the viewport
          const randomX = Math.random() * window.innerWidth;
          const randomY = Math.random() * window.innerHeight;
          smiley.style.left = `${randomX}px`;
          smiley.style.top = `${randomY}px`;

          smileyContainer.appendChild(smiley);

          // Remove the smiley after the animation ends
          setTimeout(() => {
              smiley.style.opacity = 0;
              setTimeout(() => {
                  smileyContainer.removeChild(smiley);
              }, 2000);
          }, 2000);
      }
  }
