package Runner101::Helpers;
use Exporter qw(import);
@EXPORT_OK = qw(slurp_json spew_json guess_json validate_json write_log);

use strict;
use warnings;
use File::Slurp  qw(slurp write_file);
use JSON         qw(decode_json);
use JSON::Schema;
use POSIX        qw(strftime);


sub slurp_json
{
    my ($path) = @_;
    my  $json  = slurp $path // die "Can't read $_: $!";
    decode_json $json
}


sub spew_json
{
    my ($path, $content) = @_;
    write_file $path, JSON->new->utf8->pretty->encode($content)
}


sub guess_json
{
    my $thing = @_ ? $_[0] : $_;
    if (ref $thing)
    {   $thing             } # already decoded
    elsif ($thing =~ /^\s*[\{\[]/)
    {   decode_json $thing } # JSON string
    else
    {   slurp_json  $thing } # path
}


sub validate_json
{
    my $json = guess_json($_[0]);
    my $val  = JSON::Schema->new(guess_json($_[1]))->validate($json);
    die join "\n - ", "$_[0] is invalid:", $val->errors if not $val;
    $json
}


sub write_log
{
    my $out = ref $_[0] ? shift : \*STDOUT;
    print $out strftime('[%Y-%m-%d %H:%M:%S] ', localtime), @_, "\n";
}


1
__END__

=head1 Runner101::Helpers

Contains a few helper functions used in various places of the runner.

=head2 slurp_json

    slurp_json($path)

Reads the contents of the file given in C<$path> and JSON-decodes its content.
Returns the decoding result or dies if an error reading or decoding occurs.

=head2 spew_json

    spew_json($path, $content)

JSON-encodes the given C<$content> and writes it to the file at C<$path>.
Returns nothing useful and dies if an error encoding or writing the file occurs.

=head2 guess_json

    guess_json($thing = $_)

C<$thing> may either be a reference, a JSON string or a file path. This
function figures out which kind of C<$thing> it was given and JSON-decodes it
into a data structure. Returns the result and dies on error.

Defaults to C<$_> if C<$thing> is not given.

More specifically, if C<$thing> is a reference, it is assumed to be already
decoded and it is returned unchanged. Otherwise, if it's a string with the
first non-whitespace character being C<{> or C<[>, it is assumed to be a JSON
object or array respectively (JSON only supports those two as top-level
structures) and is JSON-decoded. If that's also not the case, it is assumed to
be a file path and it is L</slurp_json>'d.

=head2 validate_json

    validate_json($json, $schema)

Validates C<$json> against the given JSON-C<$schema>. Both parameters are
L</guess_json>'d, so they may each be a hash, an array, a JSON string or a path
to a JSON file.

Returns the (decoded, if necessary) C<$json> on successful validation and dies
with a diagnostic message on validation failure.

=head2 write_log

    write_log(@message)
    write_log($out, @message)

Prints the current date, followed by C<@message>, to the given C<$out>
filehandle or, if no filehandle is given, to C<STDOUT>.

=cut
