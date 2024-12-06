import subprocess

def query_certificates(domains):
    results = {}
    
    for domain in domains:
        try:
            # 使用 curl 命令查询证书
            command = f"curl -s https://crt.sh/?q=%.{domain} | grep '{domain}' | cut -d '>' -f2 | cut -d '<' -f1 | grep -v ' ' | sort -u"
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
            results[domain] = output.strip().split('\n') if output else []
        except subprocess.CalledProcessError as e:
            print(f"Error querying {domain}: {e}")
            results[domain] = []  # 记录错误时的空结果
    
    return results

def write_results_to_file(results, output_file):
    with open(output_file, 'w') as f:
        for domain, certs in results.items():
            f.write(f"Domain: {domain}\n")
            if certs:
                for cert in certs:
                    f.write(f"  - {cert}\n")
            else:
                f.write("  - No certificates found.\n")
            f.write("\n")

if __name__ == "__main__":
    # 从文件中读取域名
    with open('domains.txt', 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    # 查询证书并写入结果
    results = query_certificates(domains)
    write_results_to_file(results, 'certificates_output.txt')

    print("查询完成，结果已写入 certificates_output.txt")
