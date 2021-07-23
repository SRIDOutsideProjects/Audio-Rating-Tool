import login from '@/views/Login'

export default [
///here we will put our routes
{
    path: 'login',
    name: 'login',  /// This name is not related to component name.. it is named routes
    component: login,
  }
//   {
//     path: '/register',
//     name: 'register',
//     component: register,
//   },
]