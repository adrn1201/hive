const searchForm = document.querySelector("#searchForm");
const pageLinks = document.querySelectorAll(".page-link");

console.log('test')
if (searchForm) {
    for (const link of pageLinks) {
        link.addEventListener("click", function(e) {
            e.preventDefault();

            let page = this.dataset.page;

            searchForm.innerHTML += `<input type="hidden" name="page" value="${page}" />`;

            searchForm.submit();
        });
    }
}