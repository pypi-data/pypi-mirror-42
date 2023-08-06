if ( !params.spadesMinCoverage{{ param_id }}.toString().isNumber() ){
    exit 1, "'spadesMinCoverage{{ param_id }}' parameter must be a number. Provided value: '${params.spadesMinCoverage{{ param_id }}}'"
}
if ( !params.spadesMinKmerCoverage{{ param_id }}.toString().isNumber()){
    exit 1, "'spadesMinKmerCoverage{{ param_id }}' parameter must be a number. Provided value: '${params.spadesMinKmerCoverage{{ param_id }}}'"
}

IN_spades_opts_{{ pid }} = Channel.value(
    [params.spadesMinCoverage{{ param_id }},
     params.spadesMinKmerCoverage{{ param_id }}
     ])

if ( params.spadesKmers{{ param_id }}.toString().split(" ").size() <= 1 ){
    if (params.spadesKmers{{ param_id }}.toString() != 'auto'){
        exit 1, "'spadesKmers{{ param_id }}' parameter must be a sequence of space separated numbers or 'auto'. Provided value: ${params.spadesKmers{{ param_id }}}"
    }
}
IN_spades_kmers_{{pid}} = Channel.value(params.spadesKmers{{ param_id }})

clear = params.clearInput{{ param_id }} ? "true" : "false"
disable_rr = params.disableRR{{ param_id }} ? "true" : "false"

checkpointClear_{{ pid }} = Channel.value(clear)
disableRR_{{ pid }} = Channel.value(disable_rr)

process spades_{{ pid }} {

    // Send POST request to platform
    {% include "post.txt" ignore missing %}

    tag { sample_id }
    publishDir 'results/assembly/spades_{{ pid }}/', pattern: '*_spades*.fasta', mode: 'copy'
    publishDir "results/assembly/spades_{{ pid }}/$sample_id", pattern: "*.gfa", mode: "copy"
    publishDir "results/assembly/spades_{{ pid }}/$sample_id", pattern: "*.fastg", mode: "copy"

    input:
    set sample_id, file(fastq_pair), max_len from {{ input_channel }}.join(SIDE_max_len_{{ pid }})
    val opts from IN_spades_opts_{{ pid }}
    val kmers from IN_spades_kmers_{{ pid }}
    val clear from checkpointClear_{{ pid }}
    val disable_rr from disableRR_{{ pid }}

    output:
    set sample_id, file('*_spades*.fasta') into {{ output_channel }}
    file "*.fastg" optional true
    file "*.gfa" into gfa1_{{ pid }}
    {% with task_name="spades" %}
    {%- include "compiler_channels.txt" ignore missing -%}
    {% endwith %}

    script:
    template "spades.py"

}

{{ forks }}

