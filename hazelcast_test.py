import hazelcast


def read_keys(name):
    client = hazelcast.HazelcastClient(cluster_name="dev",)
    my_map = client.get_map(name).blocking()
    for key, value in my_map.entry_set():
        print(key, value)


def add_keys(name, n):
    client = hazelcast.HazelcastClient(cluster_name="dev",)
    my_map = client.get_map(name).blocking()
    for i in range(n):
        my_map.put(i, i)


def increment_key(name):
    client = hazelcast.HazelcastClient(cluster_name="dev", )
    my_map = client.get_map(name).blocking()
    if not my_map.contains_key("key"):
        my_map.put("key", 0)

    for _ in range(10_000):
        value = my_map.get("key")
        value += 1
        my_map.put("key", value)


def pessimistic_increment(name):
    client = hazelcast.HazelcastClient(cluster_name="dev", )
    my_map = client.get_map(name).blocking()
    if not my_map.contains_key("key"):
        my_map.put("key", 0)

    for _ in range(10_000):
        my_map.lock("key")
        try:
            value = my_map.get("key")
            value += 1
            my_map.put("key", value)
        finally:
            my_map.unlock("key")


def optimistic_increment(name):
    client = hazelcast.HazelcastClient(cluster_name="dev", )
    my_map = client.get_map(name).blocking()
    if not my_map.contains_key("key"):
        my_map.put("key", 0)

    for _ in range(10_000):
        while True:
            value = my_map.get("key")
            new_value = value + 1
            if my_map.replace_if_same("key", value, new_value):
                break


def create_queue(name):
    client = hazelcast.HazelcastClient(cluster_name="dev", )
    my_queue = client.get_queue(name).blocking()
    my_queue.offer("item")


if __name__ == "__main__":
    # add_keys("my-map", 1000)
    # read_keys("my-map")
    # increment_key("my-map")
    # pessimistic_increment("my-map")
    # optimistic_increment("my-map")
    # read_keys("my-map")
    create_queue("queue")
