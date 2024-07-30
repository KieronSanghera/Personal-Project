// import AcmeLogo from '@/app/ui/acme-logo';
// import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from "next/link"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-6">
      <div className="flex h-20 shrink-0 items-end rounded-lg bg-blue-700 p-4 md:h-52">
        <p className={`text-xl text-white md:text-6xl md:leading-normal`}>
          <strong>Welcome to Kieron's Cloud Storage.</strong>
        </p>
      </div>
      <div className="mt-4 flex grow flex-col gap-4 md:flex-row">
        <div className="flex flex-col justify-center gap-6 rounded-lg bg-gray-50 px-6 py-10 md:w-2/5 md:px-20">
          <p className={`text-xl text-gray-800 md:text-3xl md:leading-normal`}>
            A Personal Project to showcase and further develop my skills.
          </p>
          <p className={`text-xl text-gray-800 md:text-3xl md:leading-normal`}>
            Allows users to upload files, have them stored and scanned for complete convenience.
          </p>
          <p className={`text-xl text-gray-800 md:text-3xl md:leading-normal`}>
            Click below to access the dashboard.
          </p>
          <Link
            href="/dashboard"
            className="flex items-center gap-5 self-start rounded-lg bg-blue-700 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-400 md:text-base"
          >
            <span>Go to Dashboard</span>
          </Link>
        </div>
        <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12"></div>
      </div>
    </main>
  )
}
