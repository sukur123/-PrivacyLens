#!/usr/bin/env python3
"""
PrivacyLens CLI Tool
A command-line tool for analyzing website privacy and security headers.
"""

import click
import json
import sys
from .analyzer import PrivacyAnalyzer
from .reporter import Reporter
from .utils import validate_url


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """PrivacyLens - Website Privacy & Security Analyzer"""
    pass


@cli.command()
@click.argument('url')
@click.option('--output', '-o', type=click.Choice(['text', 'json']), default='text',
              help='Output format (text or json)')
@click.option('--save', '-s', type=click.Path(), help='Save report to file')
@click.option('--timeout', '-t', default=10, help='Request timeout in seconds')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def check(url, output, save, timeout, verbose):
    """Analyze privacy and security of a website"""
    
    # Validate URL
    if not validate_url(url):
        click.echo(click.style('❌ Invalid URL format', fg='red'), err=True)
        sys.exit(1)
    
    try:
        # Initialize analyzer
        analyzer = PrivacyAnalyzer(timeout=timeout, verbose=verbose)
        
        # Perform analysis
        if verbose:
            click.echo(f"🔍 Analyzing {url}...")
        
        result = analyzer.analyze(url)
        
        # Generate report
        reporter = Reporter(output_format=output)
        report = reporter.generate_report(result)
        
        # Output report
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(report)
            click.echo(f"📄 Report saved to {save}")
        else:
            click.echo(report)
            
    except KeyboardInterrupt:
        click.echo(click.style('\n⚠️ Analysis interrupted by user', fg='yellow'), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f'❌ Analysis failed: {str(e)}', fg='red'), err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--output', '-o', type=click.Choice(['text', 'json']), default='text',
              help='Output format')
@click.option('--save-dir', '-d', type=click.Path(exists=True), help='Directory to save reports')
@click.option('--timeout', '-t', default=10, help='Request timeout in seconds')
def batch(urls, output, save_dir, timeout):
    """Analyze multiple websites in batch"""
    
    results = []
    analyzer = PrivacyAnalyzer(timeout=timeout)
    reporter = Reporter(output_format=output)
    
    for i, url in enumerate(urls, 1):
        click.echo(f"[{i}/{len(urls)}] Analyzing {url}...")
        
        try:
            result = analyzer.analyze(url)
            results.append(result)
            
            if save_dir:
                # Save individual report
                filename = f"privacy_report_{result['domain']}.{output}"
                filepath = f"{save_dir}/{filename}"
                
                report = reporter.generate_report(result)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
                    
                click.echo(f"  ✅ Report saved to {filepath}")
            else:
                # Show summary
                score = result.get('privacy_score', 0)
                status = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
                click.echo(f"  {status} Score: {score}/100")
                
        except Exception as e:
            click.echo(f"  ❌ Failed: {str(e)}")
            continue
    
    if not save_dir and output == 'json':
        # Print combined JSON results
        click.echo(json.dumps(results, indent=2))


if __name__ == '__main__':
    cli()
