var mix = {
    methods: {
        setTag (id) {
            this.topTags = this.topTags.map(tag => {
                return  tag.id === id
                    ? {
                        ...tag,
                        selected: !tag.selected
                    }
                    : tag
            })
            this.getCatalogs()
        },
        setSort (id) {
            if (this.selectedSort?.id === id) {
                this.selectedSort.selected =
                    this.selectedSort.selected === 'dec'
                        ? 'inc'
                        : 'dec'
            } else {
                if (this.selectedSort) {
                    this.selectedSort = null
                }
                this.selectedSort = this.sortRules.find(sort => sort.id === id)
                this.selectedSort = {
                    ...this.selectedSort,
                    selected: 'dec'
                }
            }
            this.getCatalogs()
        },
        getTags() {
            this.getData('/api/tags', { category: this.category })
                .then(data => this.topTags = data.map(tag => ({
                    ...tag,
                    selected: false
                })))
                .catch(() => {
                        this.topTags = this.topTags.map(tag => ({
                        ...tag,
                        selected: false
                    }))
                })
        },
        getCatalogs(page) {
            if(typeof page === "undefined") {
                page = 1
            }
            const PAGE_LIMIT = 20
            const tags = this.topTags.filter(tag => !!tag.selected).map(tag => tag.id)
            this.getData("/api/catalog", {
                page,
                category: this.category,
                sort: this.selectedSort ? this.selectedSort.id : null,
                sortType: this.selectedSort ? this.selectedSort.selected : null,
                filter: this.filter,
                tags,
                limit: PAGE_LIMIT
            })
                .then(data => {
                    throw new Error('break')
                    this.catalogCards = data.items
                    this.currentPage = data.currentPage
                    this.lastPage = data.lastPage
                    console.log(this.catalogCards)

                }).catch(() => {
                    let items = this.catalogFromServer
                        .filter(item => this.category ? item.category === this.category : true)
                    if (this.filter) {
                        if (this.filter.minPrice) {
                           items = items.filter(item => item.price >= this.filter.minPrice)
                        }
                        if (this.filter.maxPrice) {
                           items = items.filter(item => item.price <= this.filter.maxPrice)
                        }
                        if (this.filter.name) {
                            items = items.filter(item => item.title
                                .toLowerCase()
                                .indexOf(this.filter.name.trim().toLowerCase()) >= 0
                            )
                        }
                        if (this.filter.freeDelivery) {
                            items = items.filter(item => item.freeDelivery)
                        }
                        if (this.filter.available) {
                            items = items.filter(item => item.count > 0)
                        }
                    }
                    if (tags.length) {
                        items = items
                            .filter(
                                item => tags.every(
                                    tag => item.tags?.includes(tag)
                                )
                            )
                    }

                    this.pages = Math.ceil(items.length / PAGE_LIMIT)

                    if (this.selectedSort) {
                        const res = items.sort((a, b) => {
                             return this.selectedSort.selected === 'dec'
                                 ? a[this.selectedSort.id] - b[this.selectedSort.id]
                                 : b[this.selectedSort.id] - a[this.selectedSort.id]
                        })
                        items = res
                    }


                    this.catalogCards
                        = items.slice(
                            (page-1)*PAGE_LIMIT,
                            (page) * PAGE_LIMIT < (items.length - 1)
                                ? (page+1) * PAGE_LIMIT
                                : (items.length - 1)
                        )
                })
        }
    },
    mounted() {
        this.selectedSort = this.sortRules?.[1]
            ? { ...this.sortRules?.[1], selected: 'inc' }
            :  null

        this.getCatalogs()
        this.getTags()
        this.category = location.pathname.startsWith('/catalog/')
            ? Number(location.pathname.replace('/catalog/', ''))
            : null
    },
    data() {
        return {
            pages: 1,
            category: null,
            catalogCards: [],
            currentPage: null,
            lastPage: null,
            selectedSort: null,
            filter: {
                name: '',
                minPrice: 0,
                maxPrice: 50000,
                freeDelivery: false,
                available: true
            }
        }
    }
}