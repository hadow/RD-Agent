import qlib

qlib.init(provider_uri="~/.qlib/qlib_data/cn_data")

from qlib.data import D

instruments = D.instruments()
fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]

all_data = (
    D.features(instruments, fields, freq="day")
    .swaplevel()
    .sort_index()
    .loc["2008-12-29":]
    .sort_index()
)

all_data.to_hdf("./daily_pv_all.h5", key="data")


debug_data = (
    D.features(
        instruments,
        fields,
        start_time="2018-01-01",
        end_time="2019-12-31",
        freq="day",
    )
    .swaplevel()
    .sort_index()
)

# 关键修复：从 debug_data 自己里面选存在于 2018-2019 的股票
debug_instruments = debug_data.reset_index()["instrument"].drop_duplicates().to_numpy()[:100]

debug_data = (
    debug_data
    .swaplevel()
    .loc[debug_instruments]
    .swaplevel()
    .sort_index()
)

debug_data.to_hdf("./daily_pv_debug.h5", key="data")