import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-blue-800">
          <Link href="/">Nagaland Lottery Results</Link>
        </h1>
        <nav className="space-x-4">
          <Link href="/" className="text-lg text-gray-700 hover:text-blue-800">Home</Link>
          <Link href="/archive" className="text-lg text-gray-700 hover:text-blue-800">Archive</Link>
          <Link href="/contact" className="text-lg text-gray-700 hover:text-blue-800">Contact</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
