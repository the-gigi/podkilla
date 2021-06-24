import argparse
import json
import sh

k = sh.kubectl

kube_contexts = open('contexts.txt').read().replace(' ', '').split()


def kg(context, ns, kind, field_selector=None):
    """Get all resources of the specific kind

    If namespace is not provided get all resources in all namespaces

    Return the result as a Python object (parsed JSON)
    """
    args = f'{kind} --context {context} -o json'.split()
    args += ['-n', ns] if ns else ['--all-namespaces']
    if field_selector is not None:
        args += ['--field-selector=' + field_selector]
    result = k.get(*args)
    return json.loads(str(result.stdout, 'utf-8'))


def delete_failed_pods(context, reason, dry_run):
    """Delete failed pods with optional reason

    If reason is None it will delete all failed pods.
    Otherwise it will only delete failed pods with the specified reason
    """
    failed_pods = kg(context, None, 'pods', 'status.phase=Failed')['items']
    if reason is not None:
        failed_pods = [p for p in failed_pods if p['status'].get('reason') == reason]
    print('failed pods:', len(failed_pods))
    if dry_run:
        return

    for p in failed_pods:
        name = p['metadata']['name']
        namespace = p['metadata']['namespace']
        try:
            k.delete.pod(name, '--context', context, '-n', namespace)
        except Exception as e:
            print(e)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Delete failed pods with optional reason'
    )

    parser.add_argument(
        "--reason",
        help="If specified delete only pods failed with the reason",
        required=False,
        default=None
    )

    parser.add_argument(
        "--dry-run",
        help="Only print the number of failed pods. Don't delete any pod",
        action="store_true"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    action = 'Checking' if args.dry_run else 'Cleaning up'
    for context in kube_contexts:
        print(f'--- {action}', context)
        delete_failed_pods(context, args.reason, args.dry_run)


if __name__ == '__main__':
    main()
