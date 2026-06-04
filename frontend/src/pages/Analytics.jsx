import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts";

function Analytics() {

  const vendorData = [

    {
      vendor: "MedSupply",
      spend: 45000
    },

    {
      vendor: "TechCorp",
      spend: 25000
    },

    {
      vendor: "OfficePro",
      spend: 15000
    },

    {
      vendor: "CloudSys",
      spend: 12000
    }

  ];

  const statusData = [

    {
      name: "Approved",
      value: 12
    },

    {
      name: "Pending",
      value: 4
    },

    {
      name: "Rejected",
      value: 2
    }

  ];

  const COLORS = [
    "#22c55e",
    "#f59e0b",
    "#ef4444"
  ];

  return (

    <div className="mt-10">

      <h2
        className="
          text-4xl
          font-bold
          mb-8
          text-center

          bg-gradient-to-r
          from-blue-400
          to-cyan-300

          bg-clip-text
          text-transparent
        "
      >

        Procurement Analytics

      </h2>

      <div
        className="
          grid
          lg:grid-cols-2
          gap-6
        "
      >

        {/* Vendor Spend Chart */}

        <div
          className="
            bg-slate-800/70
            backdrop-blur-md
            rounded-3xl
            p-6

            border
            border-blue-500/30

            shadow-[0_0_30px_rgba(59,130,246,0.15)]
          "
        >

          <h3 className="text-xl mb-4">

            Vendor Spend Analysis

          </h3>

          <div className="h-80">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart
                data={vendorData}
              >

                <defs>

                  <linearGradient
                    id="colorSpend"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >

                    <stop
                      offset="0%"
                      stopColor="#60a5fa"
                    />

                    <stop
                      offset="100%"
                      stopColor="#2563eb"
                    />

                  </linearGradient>

                </defs>

                <XAxis
                  dataKey="vendor"
                />

                <YAxis />

                <Tooltip
                  contentStyle={{
                    backgroundColor:
                      "#0f172a",

                    border:
                      "1px solid #3b82f6",

                    borderRadius:
                      "12px",

                    boxShadow:
                      "0 0 20px rgba(59,130,246,0.5)"
                  }}
                  labelStyle={{
                    color: "#ffffff"
                  }}
                  itemStyle={{
                    color: "#60a5fa"
                  }}
                />

                <Bar
                  dataKey="spend"
                  fill="url(#colorSpend)"
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        {/* Invoice Status Pie Chart */}

        <div
          className="
            bg-slate-800/70
            backdrop-blur-md
            rounded-3xl
            p-6

            border
            border-blue-500/30

            shadow-[0_0_30px_rgba(59,130,246,0.15)]
          "
        >

          <h3 className="text-xl mb-4">

            Invoice Status Distribution

          </h3>

          <div className="h-80">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <PieChart>

                <Pie
                  data={statusData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={100}
                  label
                >

                  {statusData.map(
                    (
                      entry,
                      index
                    ) => (

                      <Cell
                        key={index}
                        fill={
                          COLORS[index]
                        }
                      />

                    )
                  )}

                </Pie>

                <Tooltip
                  contentStyle={{
                    backgroundColor:
                      "#0f172a",

                    border:
                      "1px solid #3b82f6",

                    borderRadius:
                      "12px",

                    boxShadow:
                      "0 0 20px rgba(59,130,246,0.5)"
                  }}
                  labelStyle={{
                    color: "#ffffff"
                  }}
                  itemStyle={{
                    color: "#60a5fa"
                  }}
                />

              </PieChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

    </div>

  );

}

export default Analytics;