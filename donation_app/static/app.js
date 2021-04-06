document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            function print_item_in_list(list_item, data) {
                list_item.firstElementChild.firstElementChild.innerText = data['name']
                list_item.firstElementChild.lastElementChild.innerText = data['description']
                list_item.lastElementChild.firstElementChild.innerText = data['categories']
            }

            let list_of_istitutions = e.target.parentElement.parentElement.previousElementSibling
            let first_item = list_of_istitutions.firstElementChild
            let second_item = first_item.nextElementSibling
            let third_item = second_item.nextElementSibling


            fetch('/?' + new URLSearchParams({
                foundation_page: parseInt(page),
                }), {
                    headers: {
                        'X-Requested-With': 'XMLHttpResponse'
                    },
                    method: 'get'
                })
                .then(res => res.json())
                .then(res=>{
                    console.log(res);
                    print_item_in_list(first_item, res['el0'])
                    print_item_in_list(second_item, res['el1'])
                })


            console.log(first_item, second_item, third_item);

            console.log(list_of_istitutions);

        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            let summary_div = document.querySelector(".summary");
            let items_and_institution_div = summary_div.querySelector('.form-section');
            let address_ul = items_and_institution_div.nextElementSibling.querySelector('ul')
            let date_ul = address_ul.parentElement.nextElementSibling.querySelector('ul');

            let form_steps = document.querySelectorAll("div[data-step]");
            let form_step1 = form_steps[0] //given items
            let form_step2 = form_steps[1] //number of bags
            let form_step3 = form_steps[2] //institution
            let form_step4 = form_steps[3] // address and date

            let summary_item1 = items_and_institution_div.querySelector("ul").firstElementChild.lastElementChild;
            let summary_item2 = items_and_institution_div.querySelector("ul").lastElementChild.lastElementChild;
            let num_of_bags = form_step2.querySelector('div').firstElementChild.firstElementChild.value;
            let checkboxes = document.querySelectorAll("input[type='checkbox']");

            let categories_checked = []
            checkboxes.forEach(el => {
                if (el.checked === true) {
                    categories_checked.push(el.parentElement.lastElementChild.innerText)
                }
            })

            let categories_checked_id = []
            checkboxes.forEach(el => {
                if (el.checked === true) {
                    categories_checked_id.push(el.value)
                }
            })

            let institutions = form_step3.querySelectorAll("input[type='radio']");
            let institution_checked = ''
            institutions.forEach(el => {
                if (el.checked === true) {
                    institution_checked = el;
                }
            })

            if (form_step3.classList.contains("active")) {

                console.log(categories_checked_id);

                institutions.forEach(institution => {
                    let inst_categories = institution.dataset.categories.split(" ");
                    console.log(institution.dataset.categories);
                    console.log(inst_categories);
                    categories_checked_id.forEach(checked_category => {
                        if (!inst_categories.includes(checked_category)) {
                            institution.parentElement.parentElement.style.display = 'none'
                        }
                    })
                })


            }

            if (form_step4.classList.contains("active")) {
                summary_item1.innerText = num_of_bags + ' worki zawierające ' + categories_checked.join(', ')
                summary_item2.innerText = 'Dla ' + institution_checked.parentElement.lastElementChild.firstElementChild.innerText
                let address_list_items = address_ul.querySelectorAll('li');
                let address_inputs_form = form_step4.querySelectorAll('input')
                let notices = form_step4.querySelector("textarea");
                let date_list_items = date_ul.querySelectorAll('li')

                address_list_items[0].innerText = address_inputs_form[0].value;
                address_list_items[1].innerText = address_inputs_form[1].value;
                address_list_items[2].innerText = address_inputs_form[2].value;
                address_list_items[3].innerText = address_inputs_form[3].value;
                date_list_items[0].innerText = address_inputs_form[4].value;
                date_list_items[1].innerText = address_inputs_form[5].value;
                date_list_items[2].innerText = notices.value;
            }

        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
            // let str = $("#donate-form").serializeArray();
            // console.log(str);
            // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            // // tutaj fetch
            // fetch('/donate/', {
            //     method: 'post',
            //     headers: {'X-CSRFToken': csrftoken},
            //     body: str,
            // })

            $.ajax({
                    url: '/donate/',
                    data: $('#donate-form').serializeArray(),
                    method: "POST",
                    dataType: "json",
                    success: function (response) {
                        window.location.href = response.url_success;
                    }
                }
            )
        }


    }


    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }


    /**
     Hiding istitutions
     */


});
