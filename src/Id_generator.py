import time


class SnowflakeGenerator:
    def __init__(self, node_id):
        self.node_id = node_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate_id(self):
        timestamp = int(time.time() * 1000)

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                timestamp = self.wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        snowflake_id = (timestamp << 22) | (self.node_id << 12) | self.sequence
        snowflake_id_str = self.encode_base36(snowflake_id)
        return snowflake_id_str

    def wait_for_next_millis(self, last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

    def encode_base36(self, number):
        chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        base36 = ''
        while number > 0:
            number, i = divmod(number, 36)
            base36 = chars[i] + base36
        return base36


if __name__ == '__main__':

    # Example usage:
    snowflake_generator = SnowflakeGenerator(node_id=1)

    # Generate 5 Snowflake IDs
    for _ in range(5):
        print(snowflake_generator.generate_id())
