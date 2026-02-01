import { verifySession } from '@/app/lib/dal'
import { redirect } from 'next/navigation'
import AdminDashboard from '../components/AdminDashboard'
import UserDashboard from '../components/UserDashboard'
 
export default async function Dashboard() {
  const session = await verifySession()
  const userRole = session?.role
 
  if (userRole === 'admin') {
    return <AdminDashboard />
  } else if (userRole === 'user') {
    return <UserDashboard />
  } else {
    redirect('/login')
  }
}