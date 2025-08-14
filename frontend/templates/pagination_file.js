const postsPerPage = 9;
const postGrid = document.getElementById("post-grid");
const pagination = document.getElementById("pagination");
let currentPage = 1;

function renderPosts(page) {
  postGrid.innerHTML = ""; // Clear existing posts
  const start = (page - 1) * postsPerPage;
  const end = start + postsPerPage;
  const pagePosts = posts.slice(start, end);

  pagePosts.forEach(post => {
    const col = document.createElement("div");
    col.className = "col-md-4 post-card";
    col.innerHTML = `
      <div class="card h-100 shadow-sm border-0 d-flex flex-column">
        ${post.image_url
          ? `<img src="${post.image_url}" class="card-img-top" alt="${post.title}" />`
          : `<div class="bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
               <span class="text-muted">No Image</span>
             </div>`
        }
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${post.title}</h5>
          <p class="card-text text-muted">${post.description}</p>
          <div class="mt-auto">
            <a href="/posts/${post.id}/" class="btn btn-primary btn-sm"><i class="fas fa-eye"></i> View</a>
          </div>
        </div>
      </div>`;
    postGrid.appendChild(col);
  });
  updatePagination();
}

function updatePagination() {
  pagination.innerHTML = "";
  const totalPages = Math.ceil(posts.length / postsPerPage);

  // Prev
  const prevLi = document.createElement("li");
  prevLi.className = "page-item" + (currentPage === 1 ? " disabled" : "");
  prevLi.innerHTML = `<a class="page-link" href="#" aria-label="Previous">&laquo;</a>`;
  prevLi.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage > 1) {
      currentPage--;
      renderPosts(currentPage);
    }
  });
  pagination.appendChild(prevLi);

  // Page numbers
  for (let i = 1; i <= totalPages; i++) {
    const li = document.createElement("li");
    li.className = "page-item" + (i === currentPage ? " active" : "");
    li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
    li.addEventListener("click", e => {
      e.preventDefault();
      currentPage = i;
      renderPosts(currentPage);
    });
    pagination.appendChild(li);
  }

  // Next
  const nextLi = document.createElement("li");
  nextLi.className = "page-item" + (currentPage === totalPages ? " disabled" : "");
  nextLi.innerHTML = `<a class="page-link" href="#" aria-label="Next">&raquo;</a>`;
  nextLi.addEventListener("click", e => {
    e.preventDefault();
    if (currentPage < totalPages) {
      currentPage++;
      renderPosts(currentPage);
    }
  });
  pagination.appendChild(nextLi);
}

// On page load:
document.addEventListener("DOMContentLoaded", () => {
  renderPosts(1);
});
