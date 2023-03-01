const searchForm = document.querySelector("#searchForm");
const pageLinks = document.querySelectorAll(".page-link");



if (searchForm) {
    for (const link of pageLinks) {
        link.addEventListener("click", formData);
    }

    const filterElement = document.getElementById("filter_category");
    filterElement.addEventListener("change", formData);

    function formData(e) {
        e.preventDefault();
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        let page = ''
        if (this.dataset) {
            page = this.dataset.page;
        }

        if (urlParams.get('page') && page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${page}" />`;
        } else if (urlParams.get('page') && !page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${urlParams.get('page')}" />`;
        } else if (!urlParams.get('page') && page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${page}" />`;
        }

        if (urlParams.get('category') && this.value) {
            console.log('condition 1 checked')
            searchForm.innerHTML += `<input type="hidden" name="category" value="${this.value}" />`;
        } else if (urlParams.get('category') && !this.value) {
            console.log('condition 2 checked')
            searchForm.innerHTML += `<input type="hidden" name="category" value="${urlParams.get('category')}" />`;
        } else if (!urlParams.get('category') && this.value) {
            console.log('condition 3 checked')
            searchForm.innerHTML += `<input type="hidden" name="category" value="${this.value}" />`;
        }

        searchForm.submit();
    }
}