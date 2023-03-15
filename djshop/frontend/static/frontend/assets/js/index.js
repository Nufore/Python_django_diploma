var mix = {
    methods: {
        getBanners() {
            this.getData("/api/banners")
              .then(data => {
                this.banners = data.banners
              }).catch(() => {
                  this.banners = this.catalogFromServer.slice(0, 3)
              })
        },
        getPopularProducts() {
            this.getData("/api/products/popular")
              .then(data => {
                this.popularCards = data.products
              }).catch(() => {
                  this.popularCards = this.catalogFromServer.slice(0, 5)
            })
        },
        getLimitedProducts() {
            this.getData("/api/products/limited")
              .then(data => {
                this.limitedCards = data.products
              }).catch(() => {
                  this.limitedCards = this.catalogFromServer.slice(0, 5)
            })
        },
    },
    mounted() {
        this.getBanners();
        this.getPopularProducts();
        this.getLimitedProducts();
    },
//    created() {
//      this.getLimitedProducts()
//    },
    data() {
        return {
            banners: [],
            popularCards: [],
            limitedCards: [],
        }
    }
}