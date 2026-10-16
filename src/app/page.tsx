import Navbar from '@/components/Navbar'
import Hero from '@/components/Hero'
import FeatureGrid from '@/components/FeatureGrid'
import MeetMockup from '@/components/MeetMockup'
import PricingTable from '@/components/PricingTable'
import Footer from '@/components/Footer'

export default function HomePage() {
  return (
    <>
      <Navbar />
      <Hero />
      <FeatureGrid />
      <MeetMockup />
      <PricingTable />
      <Footer />
    </>
  )
}
