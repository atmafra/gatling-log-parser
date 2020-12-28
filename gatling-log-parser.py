import argparse
import sys

from gatling_log_parser_core import log_file_to_metrics_map, request_map_to_time_buckets, aggregate_time_buckets, \
    bucket_statistics_to_csv


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Process Gatling simulation log files')
    parser.add_argument('--path', action='store', default='.', type=str, required=False,
                        help='Path to the simulation log file', metavar='<path_to_gatling_log_file>', dest='path')
    parser.add_argument('--log-file', action='store', default='simulation.log', type=str, required=False,
                        help='Gatling simulation log file name', metavar='<log_filename>', dest='log_filename')
    parser.add_argument('--csv-file', action='store', default='simulation.csv', type=str, required=False,
                        help='Output CSV file name', metavar='<output_csv_filename>', dest='csv_filename')
    parser.add_argument('--bucket-width', action='store', default=1000, type=int, required=False,
                        help='time bucket width in milliseconds', metavar='<bucket_width_in_milliseconds>',
                        dest='bucket_width_ms')
    parser.add_argument('--verbose', action='store', type=bool, required=False, default=True,
                        help='Output execution messages in terminal', metavar='verbose', dest='verbose')
    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    request_metrics_map = log_file_to_metrics_map(path=args.path,
                                                  filename=args.log_filename,
                                                  verbose=args.verbose)

    time_buckets = request_map_to_time_buckets(request_metrics_map=request_metrics_map,
                                               bucket_width_ms=args.bucket_width_ms,
                                               verbose=args.verbose)

    bucket_statistics = aggregate_time_buckets(time_buckets=time_buckets,
                                               bucket_width_ms=args.bucket_width_ms)

    bucket_statistics_to_csv(bucket_statistics, path=args.path, filename=args.csv_filename)
