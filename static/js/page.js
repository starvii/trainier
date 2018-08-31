const PageComponent = Vue
    .extend({
        template: ''
            + '<nav class="pagination is-centered" role="navigation" aria-label="pagination">'
            + '<ul class="pagination" v-show="pageConf.totalItems > 0">'
            + '<li :class="{disabled: pageConf.currentPage == 1}" @click="prevPage()"><span>&laquo;</span></li>'
            + '<li v-for="item in pageList" track-by="$index" :class="{active: item == pageConf.currentPage, separate: item == \'...\'}" '
            + '@click="changeCurrentPage(item)">'
            + '<span v-text="item"></span></li>'
            + '<li :class="{disabled: pageConf.currentPage == pageConf.numberOfPages}" @click="nextPage()"><span>&raquo;</span></li>'
            + '</ul>'
            + '<div class="page-total" v-show="pageConf.totalItems > 0">'
            + '第<input type="text" v-model="jumpPageNum" @keyup.enter="jumpToPage($event)"/>页 '
            + '每页<select v-model="pageConf.itemsPerPage"><option v-for="option in pageConf.perPageOptions">{{option}}</option></select>'
            + '/共<strong v-text="pageConf.totalItems"></strong>条'
            + '</div>'
            + '<div class="no-items" v-show="pageConf.totalItems <= 0">暂无数据</div>'
            + '</nav>',
        replace: true,
        props: {
            pageConf: {
                type: Object,
                require: true,
            },
        },
        data: {
            jumpPageNum: '',
            pageList: [],
        },
        // props: [{
        //     name: 'pageConf',
        //     require: true
        // }, 'jumpPageNum', 'pageList'],
        // props: [
        //     'pageConf',
        //     'jumpPageNum',
        //     'pageList',
        // ],
        ready: function () {
            this.pageConf.pagesLength = parseInt(this.pageConf.pagesLength) ? parseInt(this.pageConf.pagesLength)
                : 9;
            if (this.pageConf.pagesLength % 2 === 0) {
                // 如果不是奇数的时候处理一下
                this.pageConf.pagesLength = this.pageConf.pagesLength - 1;
            }

            // pageConf.perPageOptions
            if (this.pageConf.perPageOptions) {
                this.pageConf.perPageOptions = [10, 15, 30, 50, 100];
            }

            this.$watch(this.getWatchState, this.getPagination);
            this.getPagination();
        },
        methods: {
            changeCurrentPage: function (item) {
                if (item === '...') {
                    // return;
                } else {
                    this.pageConf.currentPage = item;
                }
            },

            // pageList数组
            getPagination: function (newValue, oldValue) {

                // pageConf.currentPage
                this.pageConf.currentPage = parseInt(this.pageConf.currentPage) ? parseInt(this.pageConf.currentPage)
                    : 1;

                // pageConf.totalItems
                this.pageConf.totalItems = parseInt(this.pageConf.totalItems) ? parseInt(this.pageConf.totalItems)
                    : 0;

                // pageConf.itemsPerPage (default:15)
                this.pageConf.itemsPerPage = parseInt(this.pageConf.itemsPerPage) ? parseInt(this.pageConf.itemsPerPage)
                    : 15;

                // numberOfPages
                this.pageConf.numberOfPages = Math.ceil(this.pageConf.totalItems
                    / this.pageConf.itemsPerPage);

                // judge currentPage > numberOfPages
                if (this.pageConf.currentPage < 1) {
                    this.pageConf.currentPage = 1;
                }

                // 如果分页总数>0，并且当前页大于分页总数
                if (this.pageConf.numberOfPages > 0
                    && this.pageConf.currentPage > this.pageConf.numberOfPages) {
                    this.pageConf.currentPage = this.pageConf.numberOfPages;
                }

                // jumpPageNum
                this.jumpPageNum = this.pageConf.currentPage;

                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                let perPageOptionsLength = this.pageConf.perPageOptions.length;
                // 定义状态
                let perPageOptionsStatus;
                for (var i = 0; i < perPageOptionsLength; i++) {
                    if (this.pageConf.perPageOptions[i] === this.pageConf.itemsPerPage) {
                        perPageOptionsStatus = true;
                    }
                }
                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                if (!perPageOptionsStatus) {
                    this.pageConf.perPageOptions.push(this.pageConf.itemsPerPage);
                }

                // 对选项进行sort
                this.pageConf.perPageOptions.sort(function (a, b) {
                    return a - b
                });

                this.pageList = [];
                if (this.pageConf.numberOfPages <= this.pageConf.pagesLength) {
                    // 判断总页数如果小于等于分页的长度，若小于则直接显示
                    for (i = 1; i <= this.pageConf.numberOfPages; i++) {
                        this.pageList.push(i.toString());
                    }
                } else {
                    // 总页数大于分页长度（此时分为三种情况：1.左边没有···2.右边没有···3.左右都有···）
                    // 计算中心偏移量
                    let offset = (this.pageConf.pagesLength - 1) / 2;
                    if (this.pageConf.currentPage <= offset) {
                        // 左边没有···
                        for (i = 1; i <= offset + 1; i++) {
                            this.pageList.push(i);
                        }
                        this.pageList.push('...');
                        this.pageList.push(this.pageConf.numberOfPages);
                    } else if (this.pageConf.currentPage > this.pageConf.numberOfPages
                        - offset) {
                        this.pageList.push(1);
                        this.pageList.push('...');
                        for (i = offset + 1; i >= 1; i--) {
                            this.pageList.push(this.pageConf.numberOfPages - i);
                        }
                        this.pageList.push(this.pageConf.numberOfPages);
                    } else {
                        // 最后一种情况，两边都有...
                        this.pageList.push(1);
                        this.pageList.push('...');

                        for (i = Math.ceil(offset / 2); i >= 1; i--) {
                            this.pageList.push(this.pageConf.currentPage - i);
                        }
                        this.pageList.push(this.pageConf.currentPage);
                        for (i = 1; i <= offset / 2; i++) {
                            this.pageList.push(this.pageConf.currentPage + i);
                        }

                        this.pageList.push('...');
                        this.pageList.push(this.pageConf.numberOfPages);
                    }
                }

                // 防止初始化两次请求问题
                let functionOnChange;
                if (this.pageConf.onChange) {
                    if (this.$parent.$options.methods[this.pageConf.onChange]) {
                        functionOnChange = this.$parent.$options.methods[this.pageConf.onChange];
                    }
                }
                if (functionOnChange) {
                    if (!(oldValue !== newValue && oldValue[0] === 0)) {
                        functionOnChange.apply(this.$parent);
                    }
                }
            },

            prevPage: function () {
                if (this.pageConf.currentPage > 1) {
                    this.pageConf.currentPage -= 1;
                }
            },

            nextPage: function () {
                if (this.pageConf.currentPage < this.pageConf.numberOfPages) {
                    this.pageConf.currentPage += 1;
                }
            },

            jumpToPage: function () {
                let pn = this.jumpPageNum.toString().replace(/[^0-9]/g, '');
                if (pn !== '') {
                    this.jumpPageNum = parseInt(pn);
                    this.pageConf.currentPage = parseInt(pn);
                }
            },

            getWatchState: function () {
                if (!this.pageConf.totalItems) {
                    this.pageConf.totalItems = 0;
                }
                let watchState = this.pageConf.totalItems + ' '
                    + this.pageConf.currentPage + ' '
                    + this.pageConf.itemsPerPage;
                return watchState;
            },
        },
    });

Vue.component('page-component', PageComponent);
