let slideshowContainer = document.querySelector(".slideshow-container");
let slides = document.querySelectorAll(".slide");
let slideIndex = 0;

showSlides();

function showSlides() {
  for (let i = 0; i < slides.length; i++) {
    slides[i].classList.remove("active");
    slides[i].classList.add("hidden");
  }

  for (let i = slideIndex; i < slideIndex + 4; i++) {
    if (i < slides.length) {
      slides[i].classList.add("active");
      slides[i].classList.remove("hidden");
    }
  }
}

function changeSlide(n) {
  slideIndex += n;
  
  if (slideIndex >= slides.length-3) {
    slideIndex = 0;
  } else if (slideIndex < 0 &&  n == -1) {
    slideIndex = slides.length - 4;
  } else if (slideIndex < 0) {
    slideIndex = slides.length - 3;
  }
  
  showSlides();
}

// 버튼을 눌렀을떄
document.querySelectorAll('.search-scope-btn').forEach(btn => {
  btn.addEventListener('click', (event) => {
    event.preventDefault(); // 기본 이벤트 동작 취소
    const selectedScope = event.target.dataset.searchScope; // 선택한 검색 범위
    const dropdownBtn = document.querySelector('.dropbtn'); // 드롭다운 버튼
    dropdownBtn.textContent = event.target.textContent; // 드롭다운 버튼의 이름 변경
  });
});

// Get the search input and selected-allergens element
const searchInput = document.getElementById('search-input');
const selectedAllergens = document.getElementById('selected-allergens');
const allergenBtnsContainer = document.getElementById('allergen-btns-container');

// Add event listener to allergen buttons
const allergenBtns = document.querySelectorAll('.allergen-btn');
allergenBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // Get the selected allergen and add to selected-allergens element
    const allergen = btn.getAttribute('data-allergen');
    
    // Check if the hashtag already exists and add it only if it does not exist
    const hashtagExists = [...selectedAllergens.querySelectorAll('.hashtag')].some(hashtag => hashtag.textContent === `#${allergen}`);
    if (!hashtagExists) {
      const hashtag = document.createElement('span');
      hashtag.classList.add('hashtag');
      hashtag.textContent = `#${allergen}`;
      selectedAllergens.appendChild(hashtag);
    }

    // Clear the search input and add the selected allergen to the query string
    searchInput.value = '';
    const params = new URLSearchParams(window.location.search);
    params.set('allergen', allergen);
    window.location.search = params.toString();
  });
});

// Add event listener to hashtags for deselecting allergens
selectedAllergens.addEventListener('click', e => {
  if (e.target.classList.contains('hashtag')) {
    // Remove the hashtag and update the query string
    const allergen = e.target.textContent.slice(1);
    e.target.remove();
    const params = new URLSearchParams(window.location.search);
    params.delete('allergen');
    window.location.search = params.toString();
  }
});

// Fill the search input with the selected allergen on page load
const params = new URLSearchParams(window.location.search);
const allergen = params.get('allergen');
if (allergen) {
  const hashtag = document.createElement('span');
  hashtag.classList.add('hashtag');
  hashtag.textContent = `#${allergen}`;
  selectedAllergens.appendChild(hashtag);
  searchInput.value = allergen;
}

// Append the allergen buttons container to the search form
const searchForm = document.querySelector('.search form');
searchForm.appendChild(allergenBtnsContainer);


let myText = "{알러지}를 제외한 {음식}의 레시피는 ---입니다."
document.getElementByID("recommend").innerHTML = myText;

///////////////////////

const ITEMS_PER_PAGE = 20; // 한 페이지당 보여줄 아이템의 수
const postList = document.getElementById('post-list'); // 게시글 리스트
const pagination = document.querySelector('.pagination'); // 페이지네이션 컨테이너

// 총 게시글 수가 주어졌을 때, 필요한 페이지 수를 계산하는 함수
function getPageCount(totalItems) {
  return Math.ceil(totalItems / ITEMS_PER_PAGE);
}

// 페이지네이션 버튼을 만드는 함수
function createPaginationButtons(pageCount, currentPage) {
  const buttons = []; // 버튼들을 담을 배열
  const maxVisibleButtons = 5; // 페이지네이션에서 보여질 최대 버튼 수
  let numLeftButtons = Math.min(currentPage - 1, Math.floor(maxVisibleButtons / 2)); // 현재 페이지 왼쪽에 보여줄 버튼의 수
  let numRightButtons = Math.min(pageCount - currentPage, Math.ceil(maxVisibleButtons / 2)); // 현재 페이지 오른쪽에 보여줄 버튼의 수

  // 왼쪽 버튼 추가
  for (let i = currentPage - numLeftButtons; i < currentPage; i++) {
    if (i > 0) {
      buttons.push(createPaginationButton(i));
    }
  }

  // 현재 페이지 버튼 추가
  buttons.push(createPaginationButton(currentPage, true));

  // 오른쪽 버튼 추가
  for (let i = currentPage + 1; i <= currentPage + numRightButtons; i++) {
    if (i <= pageCount) {
      buttons.push(createPaginationButton(i));
    }
  }

  return buttons;
}

// 페이지네이션 버튼을 만드는 함수
function createPaginationButton(pageNum, isCurrentPage = false) {
  const button = document.createElement('button');
  button.innerText = pageNum;
  button.classList.add('pagination-button');
  if (isCurrentPage) {
    button.classList.add('current-page');
    button.disabled = true;
  } else {
    button.addEventListener('click', () => handlePageChange(pageNum));
  }
  return button;
}

// 페이지를 변경하는 함수
function handlePageChange(pageNum) {
  // 선택된 페이지에 해당하는 게시글들만 보여줍니다.
  const posts = postList.querySelectorAll('tr');
  const start = (pageNum - 1) * ITEMS_PER_PAGE;
  const end = start + ITEMS_PER_PAGE;
  for (let i = 0; i < posts.length; i++) {
    if (i >= start && i < end) {
      posts[i].style.display = '';
    } else {
      posts[i].style.display = 'none';
    }
  }

  // 페이지네이션 버튼을 다시 만듭니다.
  const pageCount = getPageCount(posts.length);
  const currentPage = pageNum;
  const buttons = createPaginationButtons(pageCount, currentPage);

  // 이전 버튼, 다음 버튼 추가
  if (currentPage > 1) {
    buttons.unshift(createPaginationButton(currentPage - 1));
  }
  if (currentPage < pageCount) {
    buttons.push(createPaginationButton(currentPage + 1));
  }

// 기존 버튼들을 삭제하고 새로 만든 버튼들을 추가합니다
function renderPaginationButtons(currentPage, totalPages) {
  // pagination 요소에서 기존 버튼들을 삭제합니다
  const pagination = document.querySelector('.pagination');
  pagination.innerHTML = '';

  // 시작 페이지와 끝 페이지를 계산합니다
  const startPage = Math.max(1, currentPage - 2);
  const endPage = Math.min(totalPages, currentPage + 2);

  // 이전 버튼을 추가합니다
  const prevButton = document.createElement('button');
  prevButton.innerHTML = '이전';
  prevButton.classList.add('pagination-button');
  prevButton.disabled = (currentPage === 1);
  prevButton.addEventListener('click', () => {
    renderPage(currentPage - 1);
  });
  pagination.appendChild(prevButton);

  // 시작 페이지부터 끝 페이지까지 버튼을 추가합니다
  for (let page = startPage; page <= endPage; page++) {
    const pageButton = document.createElement('button');
    pageButton.innerHTML = page;
    pageButton.classList.add('pagination-button');
    pageButton.disabled = (page === currentPage);
    pageButton.addEventListener('click', () => {
      renderPage(page);
    });
    pagination.appendChild(pageButton);
  }

  // 다음 버튼을 추가합니다
  const nextButton = document.createElement('button');
  nextButton.innerHTML = '다음';
  nextButton.classList.add('pagination-button');
  nextButton.disabled = (currentPage === totalPages);
  nextButton.addEventListener('click', () => {
    renderPage(currentPage + 1);
  });
  pagination.appendChild(nextButton);
  }
}

const editButton = document.querySelector('.edit-button');
const username = document.querySelector('.username');

editButton.addEventListener('click', () => {
  // edit mode로 변경
  username.innerHTML = `<input type="text" value="${username.innerText}">`;
  editButton.innerHTML = '확인';
  
  const confirmButton = document.createElement('button');
  confirmButton.innerHTML = '취소';
  confirmButton.addEventListener('click', () => {
    // view mode로 변경
    username.innerHTML = `${username.firstChild.value}`;
    editButton.innerHTML = '수정';
    confirmButton.remove();
  });
  
  editButton.insertAdjacentElement('afterend', confirmButton);
});
