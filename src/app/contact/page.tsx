const ContactPage = () => {
  return (
    <div className="space-y-6 bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-3xl font-bold">Contact Us</h2>
      <p className="text-lg text-gray-700">
        If you have any questions or feedback, please feel free to reach out to us.
      </p>
      <div>
        <p className="font-semibold">Email:</p>
        <a href="mailto:contact@example.com" className="text-blue-600 hover:underline">
          contact@example.com
        </a>
      </div>
      <div>
        <p className="font-semibold">Address:</p>
        <p>123 Lottery Lane, Kohima, Nagaland, India</p>
      </div>
    </div>
  );
};

export default ContactPage;
