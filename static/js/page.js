const PageComponent = Vue
    .extend({
        template: ''
            + '<div class="pagination is-centered is-small">'
            + '<ul class="pagination-list" v-show="conf.totalItems > 0">'
            + '<li class="pagination-link" :class="{\'is-disabled\': conf.currentPage == 1}" @click="prevPage()"><span><i class="fas fa-angle-left"></i></span></li>'
            + '<li v-for="item in pageList" track-by="$index" :class="{\'is-current pagination-link\': item == conf.currentPage, \'pagination-link\': item != conf.currentPage, \'pagination-ellipsis\': item == \'...\'}"'
            + '@click="changeCurrentPage(item)">'
            + '<span v-text="item"></span></li>'
            + '<li class="pagination-link" :class="{\'is-disabled\': conf.currentPage == conf.numberOfPages}" @click="nextPage()"><span><i class="fas fa-angle-right"></i></span></li>'
            + '</ul>'
            + '<div class="page-total" v-show="conf.totalItems > 0">'
            + '<input class="input is-static is-small" type="text" value="第" style="width: 40px;" readonly>'
            + '<input class="input is-small" style="width: 40px;" type="text" v-model="jumpPageNum" @keyup.enter="jumpToPage($event)"/>'
            + '<input class="input is-static is-small" type="text" value="页" style="width: 40px;" readonly>'
            + '<input class="input is-static is-small" type="text" value="每页" style="width: 40px;" readonly>'
            + '<select class="select is-small" v-model="conf.itemsPerPage"><option v-for="option in conf.perPageOptions">{{option}}</option></select>'
            + '<input class="input is-static is-small" type="text" style="width: 60px;" readonly v-model="totalItems">'
            + '</div>'
            + '<div v-show="conf.totalItems <= 0">暂无数据</div>'
            + '</div>',
        replace: true,
        props: {
            conf: {
                type: Object,
                require: true,
            },
            // jumpPageNum: {
            //     type: String,
            //     require: false,
            // },
            // pageList: {
            //     type: Array,
            //     require: false,
            // },
        },
        data: function () {
            return {
                jumpPageNum: '',
                pageList: [],
            };
        },
        computed: {
            totalItems: function () {
                return '/共' + this.conf.totalItems + '条';
            }
        },
        // props: [{
        //     name: 'conf',
        //     require: true
        // }, 'jumpPageNum', 'pageList'],
        // props: [
        //     'conf',
        //     'jumpPageNum',
        //     'pageList',
        // ],
        mounted: function () {
            this.conf.pagesLength = parseInt(this.conf.pagesLength) ? parseInt(this.conf.pagesLength)
                : 9;
            if (this.conf.pagesLength % 2 === 0) {
                // 如果不是奇数的时候处理一下
                this.conf.pagesLength = this.conf.pagesLength - 1;
            }

            // conf.perPageOptions
            if (this.conf.perPageOptions) {
                this.conf.perPageOptions = [10, 15, 30, 50, 100];
            }

            this.$watch(this.getWatchState, this.getPagination);
            this.getPagination();
        },
        methods: {
            changeCurrentPage: function (item) {
                if (item === '...') {
                    // return;
                } else {
                    this.conf.currentPage = item;
                }
            },

            // pageList数组
            getPagination: function (newValue, oldValue) {

                // conf.currentPage
                this.conf.currentPage = parseInt(this.conf.currentPage) ? parseInt(this.conf.currentPage)
                    : 1;

                // conf.totalItems
                this.conf.totalItems = parseInt(this.conf.totalItems) ? parseInt(this.conf.totalItems)
                    : 0;

                // conf.itemsPerPage (default:15)
                this.conf.itemsPerPage = parseInt(this.conf.itemsPerPage) ? parseInt(this.conf.itemsPerPage)
                    : 15;

                // numberOfPages
                this.conf.numberOfPages = Math.ceil(this.conf.totalItems
                    / this.conf.itemsPerPage);

                // judge currentPage > numberOfPages
                if (this.conf.currentPage < 1) {
                    this.conf.currentPage = 1;
                }

                // 如果分页总数>0，并且当前页大于分页总数
                if (this.conf.numberOfPages > 0
                    && this.conf.currentPage > this.conf.numberOfPages) {
                    this.conf.currentPage = this.conf.numberOfPages;
                }

                // jumpPageNum
                this.jumpPageNum = this.conf.currentPage;

                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                let perPageOptionsLength = this.conf.perPageOptions.length;
                // 定义状态
                let perPageOptionsStatus;
                for (var i = 0; i < perPageOptionsLength; i++) {
                    if (this.conf.perPageOptions[i] === this.conf.itemsPerPage) {
                        perPageOptionsStatus = true;
                    }
                }
                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                if (!perPageOptionsStatus) {
                    this.conf.perPageOptions.push(this.conf.itemsPerPage);
                }

                // 对选项进行sort
                this.conf.perPageOptions.sort(function (a, b) {
                    return a - b
                });

                this.pageList = [];
                if (this.conf.numberOfPages <= this.conf.pagesLength) {
                    // 判断总页数如果小于等于分页的长度，若小于则直接显示
                    for (i = 1; i <= this.conf.numberOfPages; i++) {
                        this.pageList.push(i.toString());
                    }
                } else {
                    // 总页数大于分页长度（此时分为三种情况：1.左边没有···2.右边没有···3.左右都有···）
                    // 计算中心偏移量
                    let offset = (this.conf.pagesLength - 1) / 2;
                    if (this.conf.currentPage <= offset) {
                        // 左边没有···
                        for (i = 1; i <= offset + 1; i++) {
                            this.pageList.push(i);
                        }
                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    } else if (this.conf.currentPage > this.conf.numberOfPages
                        - offset) {
                        this.pageList.push(1);
                        this.pageList.push('...');
                        for (i = offset + 1; i >= 1; i--) {
                            this.pageList.push(this.conf.numberOfPages - i);
                        }
                        this.pageList.push(this.conf.numberOfPages);
                    } else {
                        // 最后一种情况，两边都有...
                        this.pageList.push(1);
                        this.pageList.push('...');

                        for (i = Math.ceil(offset / 2); i >= 1; i--) {
                            this.pageList.push(this.conf.currentPage - i);
                        }
                        this.pageList.push(this.conf.currentPage);
                        for (i = 1; i <= offset / 2; i++) {
                            this.pageList.push(this.conf.currentPage + i);
                        }

                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    }
                }

                // 防止初始化两次请求问题
                let functionOnChange;
                if (this.conf.onChange) {
                    if (this.$parent.$options.methods[this.conf.onChange]) {
                        functionOnChange = this.$parent.$options.methods[this.conf.onChange];
                    }
                }
                if (functionOnChange) {
                    if (!(oldValue !== newValue && oldValue[0] === 0)) {
                        functionOnChange.apply(this.$parent);
                    }
                }
            },

            prevPage: function () {
                if (this.conf.currentPage > 1) {
                    this.conf.currentPage -= 1;
                }
            },

            nextPage: function () {
                if (this.conf.currentPage < this.conf.numberOfPages) {
                    this.conf.currentPage += 1;
                }
            },

            jumpToPage: function () {
                let pn = this.jumpPageNum.toString().replace(/[^0-9]/g, '');
                if (pn !== '') {
                    this.jumpPageNum = parseInt(pn);
                    this.conf.currentPage = parseInt(pn);
                }
            },

            getWatchState: function () {
                if (!this.conf.totalItems) {
                    this.conf.totalItems = 0;
                }
                let watchState = this.conf.totalItems + ' '
                    + this.conf.currentPage + ' '
                    + this.conf.itemsPerPage;
                return watchState;
            },
        },
    });

Vue.component('page-component', PageComponent);
