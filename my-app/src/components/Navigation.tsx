"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    return pathname === path ? 'text-blue-500' : 'text-gray-600 hover:text-gray-900';
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link href="/" className="text-xl font-bold text-gray-900">
                DigitalDivide.ai
              </Link>
            </div>
          </div>
          <div className="flex space-x-8">
            <Link
              href="/"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/')}`}
            >
              Map
            </Link>
            <Link
              href="/directory"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/directory' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/directory')}`}
            >
              Directory
            </Link>
            <Link
              href="/about"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/about' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/about')}`}
            >
              About
            </Link>
            <Link
              href="/faq"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/faq' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/faq')}`}
            >
              FAQ
            </Link>
            <Link
              href="/get-involved"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/get-involved' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/get-involved')}`}
            >
              Get Involved
            </Link>
            <Link
              href="/developers"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/developers' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/developers')}`}
            >
              Developers
            </Link>
            <Link
              href="/blog"
              className={`inline-flex items-center px-1 pt-1 border-b-2 ${
                pathname === '/blog' ? 'border-blue-500' : 'border-transparent'
              } ${isActive('/blog')}`}
            >
              Blog
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
