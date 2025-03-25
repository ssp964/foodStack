from processing.data_ingestion_fn import (
    fetch_all_data,
    fetch_current_data,
)


if __name__ == "__main__":

    # Data ingestion Tests
    # data = fetch_all_data()
    # print(data)

    data = fetch_current_data()
    print(data)
