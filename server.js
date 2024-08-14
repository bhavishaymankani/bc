Moralis.Cloud.define("getAvgGas", async function (request) {
    // Create a query for the "EthTransactions" class
    const query = new Moralis.Query("EthTransactions");

    // Define the aggregation pipeline
    const pipeline = [
        {
            $group: {
                _id: "$from_address", // Group by "from_address"
                avgGas: {
                    $avg: {
                        $divide: ["$gas_price", 1000000000] // Convert wei to gwei
                    }
                }
            }
        },
        {
            $sort: { avgGas: -1 } // Sort by avgGas in descending order
        },
        {
            $limit: 10 // Limit results to the top 10
        }
    ];

    // Run the aggregation pipeline with master key
    const results = await query.aggregate(pipeline, { useMasterKey: true });

    return results;
});
