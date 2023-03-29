const searchForm = document.querySelector("#searchForm");
const pageLinks = document.querySelectorAll(".page-link");



if (searchForm) {
    for (const link of pageLinks) {
        link.addEventListener("click", formData);
    }

    if (window.location.pathname !== '/analytics/') {
        const filterElement = document.getElementById("filter_category");
        filterElement.addEventListener("change", formData);
    } else {
        const period = document.getElementById("period");
        if (period) {
            period.addEventListener("change", formData);
        }
        const periodTabular = document.getElementById("period_tabular");
        if (periodTabular) {
            periodTabular.addEventListener("change", formData);
        }
    }


    const predictBtns = document.querySelectorAll('.predict_btns');
    if (predictBtns) {
        for (const btns of predictBtns) {
            btns.addEventListener('click', formData)
        }
    }
    const btnVariations = document.querySelectorAll('.btn_variations');
    if (btnVariations) {
        for (const btns of btnVariations) {
            btns.addEventListener('click', formData)
        }
    }

    function formData(e) {
        e.preventDefault();
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        let page = ''
        let prod_id = ''
        let variation_id = ''
        if (this.dataset) {
            if (this.dataset.page) {
                page = this.dataset.page;
            }

            if (this.dataset.id) {
                prod_id = this.dataset.id;
            }

            if (this.dataset.variation) {
                variation_id = this.dataset.variation;
            }

        }

        if (urlParams.get('predict') && prod_id) {
            searchForm.innerHTML += `<input type="hidden" name="predict" value="${prod_id}" />`;
        } else if (urlParams.get('predict') && !prod_id) {
            searchForm.innerHTML += `<input type="hidden" name="predict" value="${urlParams.get('predict')}" />`;
        } else if (!urlParams.get('predict') && prod_id) {
            searchForm.innerHTML += `<input type="hidden" name="predict" value="${prod_id}" />`;
        }

        if (urlParams.get('variationId') && variation_id) {
            searchForm.innerHTML += `<input type="hidden" name="variationId" value="${variation_id}" />`;
        } else if (!urlParams.get('variationId') && variation_id) {
            searchForm.innerHTML += `<input type="hidden" name="variationId" value="${variation_id}" />`;
        }

        if (urlParams.get('page') && page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${page}" />`;
        } else if (urlParams.get('page') && !page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${urlParams.get('page')}" />`;
        } else if (!urlParams.get('page') && page) {
            searchForm.innerHTML += `<input type="hidden" name="page" value="${page}" />`;
        }

        if (window.location.pathname !== '/analytics/') {
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
        } else {
            if (urlParams.get('period') && this.value) {
                searchForm.innerHTML += `<input type="hidden" name="period" value="${this.value}" />`;
            } else if (urlParams.get('period') && !this.value) {
                searchForm.innerHTML += `<input type="hidden" name="period" value="${urlParams.get('period')}" />`;
            } else if (!urlParams.get('period') && this.value) {
                searchForm.innerHTML += `<input type="hidden" name="period" value="${this.value}" />`;
            }
        }

        searchForm.submit();
    }
}