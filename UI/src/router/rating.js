import Rating from "@/components/Rating"

export default [
    ///here we will put our routes
    {
        path: '/',
        name: 'rating',
        component: Rating,
        meta:{
          requiresAuth:true
        }
      },
    ]