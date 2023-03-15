var mix = {
    methods: {
        getHistoryOrder() {
            this.getData("/api/history-order")
              .then(data => {
                this.orders = data.orders
              }).catch(() => {
                this.orders = [1,2,3,4,5,6].map(val => {
                    return {
                        id: val,
                        createdAt: '2022-23-0'+val+' 13.00',
                        deliveryType: 'free shipping',
                        paymentType: 'online',
                        totalCost: 567.8,
                        status: val % 2 === 0 ? 'Подтвержден' : 'Отменен'
                    }
                })
            })
        }
    },
    mounted() {
        this.getHistoryOrder();
    },
    data() {
        return {
            orders: [],
        }
    }
}