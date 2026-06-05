import { useEffect, useState } from "react";
import api from "../services/api";

import {
  Clock,
  FileCheck,
  Building2,
  DollarSign
} from "lucide-react";

function Dashboard() {

  const [data, setData] = useState(null);

  useEffect(() => {

    api.get("/dashboard")
      .then((response) => {

        setData(response.data);

      })
      .catch((error) => {

        console.error(error);

      });

  }, []);

  if (!data) {

    return (

      <div className="p-8 text-center">

        <h2 className="text-xl text-slate-300">
          Loading Dashboard...
        </h2>

      </div>

    );

  }

  const cards = [

    {
      title: "Total Spend",
      value: `$${Number(
        data.total_spend
      ).toLocaleString("en-US")}`,
      icon: DollarSign
    },

    {
      title: "Pending Amount",
      value: `$${Number(
        data.pending_amount
      ).toLocaleString("en-US")}`,
      icon: Clock
    },

    {
      title: "Approved Invoices",
      value: data.approved_invoices,
      icon: FileCheck
    },

    {
      title: "Top Vendor",
      value: data.top_vendor,
      icon: Building2
    }

  ];

  return (

    <div className="mb-10 md:mb-12">

      <h2
        className="
          text-2xl
          md:text-4xl
          font-bold
          mb-6
          md:mb-8
          text-center

          bg-gradient-to-r
          from-blue-400
          via-cyan-300
          to-blue-500

          bg-clip-text
          text-transparent
        "
      >
        Procurement Dashboard
      </h2>

      <div
        className="
          grid
          grid-cols-1
          md:grid-cols-2
          xl:grid-cols-4
          gap-4
          md:gap-6
        "
      >

        {cards.map((card, index) => {

          const Icon = card.icon;

          return (

            <div
              key={index}
              className="
                bg-slate-800/70
                backdrop-blur-md

                rounded-3xl

                p-5
                md:p-8

                border
                border-blue-500/20

                shadow-[0_0_30px_rgba(59,130,246,0.12)]

                hover:shadow-[0_0_50px_rgba(59,130,246,0.35)]
                hover:border-blue-400
                hover:-translate-y-2

                transition-all
                duration-300
              "
            >

              <div
                className="
                  flex
                  items-center
                  justify-between

                  mb-4
                  md:mb-6
                "
              >

                <h3
                  className="
                    text-slate-300
                    uppercase
                    tracking-widest
                    text-xs
                    font-semibold
                  "
                >
                  {card.title}
                </h3>

                <Icon
                  size={26}
                  className="
                    text-blue-400
                    drop-shadow-[0_0_12px_rgba(59,130,246,0.9)]
                  "
                />

              </div>

              {card.title === "Top Vendor" ? (

                <div
                  className="
                    text-lg
                    md:text-2xl

                    font-bold
                    text-center

                    break-words

                    bg-gradient-to-r
                    from-blue-300
                    to-cyan-400

                    bg-clip-text
                    text-transparent
                  "
                >
                  {card.value}
                </div>

              ) : (

                <div
                  className="
                    text-3xl
                    md:text-4xl

                    font-extrabold

                    break-words

                    bg-gradient-to-r
                    from-blue-300
                    to-cyan-400

                    bg-clip-text
                    text-transparent
                  "
                >
                  {card.value}
                </div>

              )}

            </div>

          );

        })}

      </div>

    </div>

  );

}

export default Dashboard;